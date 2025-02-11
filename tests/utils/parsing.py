"""
This file contains functions to parse and use entities from C and C++ files
"""

from clang.cindex import Cursor, CursorKind, Index, TranslationUnit


def parse_file(input_filename: str) -> TranslationUnit:
    """
    Return the TranslationUnit for the given file
    """

    # init Index to parse file
    index = Index.create()

    return index.parse(input_filename)


def find_entities(
    node: Cursor, include_calls: bool, *entities: tuple[CursorKind, str]
) -> list[Cursor, ...]:
    """
    Find the desired entities as a list of Cursors from the supplied node
    """

    found_entities = []

    # initialize stack to use for search
    stack = [node]

    # perform depth-first search for entities
    while stack and len(found_entities) < len(entities):
        current_entity = stack.pop()

        for child in current_entity.get_children():
            if any(
                child.kind == kind and child.spelling == name
                for kind, name in entities
            ):
                # add matching entries
                found_entities.append(child)
            else:
                stack.append(child)

    if include_calls:
        # copy stack from found entities
        stack = found_entities.copy()

        while stack:
            current_entity = stack.pop()

            for child in current_entity.get_children():
                # continue search only for children in same file
                if str(child.location.file) == str(
                    current_entity.location.file
                ):
                    # check if child is call expression to ref in same file
                    if (
                        child.kind == CursorKind.CALL_EXPR
                        and child.referenced is not None
                        and str(child.referenced.location.file)
                        == str(current_entity.location.file)
                        and child.referenced not in found_entities
                    ):
                        # add call expression's reference if true
                        found_entities.append(child.referenced)
                        stack.append(child.referenced)
                    else:
                        stack.append(child)

    return found_entities


def get_cursor_range(cursor: Cursor, file_contents: str) -> tuple[int, int]:
    """
    Returns a (start, length) tuple for a Cursor by using its token
    boundaries, but then adjusts the start offset by verifying the
    token’s spelling appears in the file contents. This fixes issues
    where the token’s extent is off (e.g.
    when removing "int main(){}" the "i" of "int" was left behind).
    """
    tokens = list(cursor.get_tokens())
    if not tokens:
        return (cursor.extent.start.offset, 0)

    # Get the first token and its spelling.
    first_token = tokens[0]
    token_text = first_token.spelling
    reported_start = first_token.extent.start.offset

    # Check if the token’s spelling is actually at the reported start.
    # If not, search backwards a little bit.
    if (
        file_contents[reported_start : reported_start + len(token_text)]
        != token_text
    ):
        for offset in range(max(0, reported_start - 10), reported_start):
            if file_contents[offset : offset + len(token_text)] == token_text:
                reported_start = offset
                break

    # Use the end offset of the last token.
    end_offset = tokens[-1].extent.end.offset

    return (reported_start, end_offset - reported_start)


def get_direct_include_offsets(tu: TranslationUnit) -> tuple[int, ...]:
    """
    Returns the offsets for the inclusion directives directly in the file
    """

    return (
        x.location.offset
        for x in filter(
            lambda x: x.depth == 1, tu.get_includes()  # only direct includes
        )
    )


def get_global_ranges(node: Cursor) -> list[tuple[int, int, str]]:
    """
    Get the ranges for required "globals" (global variables and
    namespace declaration/directives)
    """

    found_entities = []

    if node.kind != CursorKind.TRANSLATION_UNIT:
        return found_entities

    for child in node.get_children():
        if child.kind in (
            CursorKind.VAR_DECL,  # global variables
            CursorKind.USING_DIRECTIVE,  # using namespace ...
            CursorKind.USING_DECLARATION,
        ):  # using ...
            found_entities.append(child)

    # store entity ranges for found requested entities
    entity_ranges = map(get_cursor_range, found_entities)

    # return ranges sorted by start position
    return sorted(entity_ranges, key=lambda x: x[0])


def get_function_ranges(
    cursor: Cursor, include_calls: bool, *function_names: str
) -> list[tuple[int, int]]:
    """
    Get the ranges for supplied functions
    """

    found_functions = find_entities(
        cursor,
        include_calls,
        *((CursorKind.FUNCTION_DECL, func) for func in function_names)
    )

    # store entity ranges for found requested functions
    function_ranges = map(get_cursor_range, found_functions)

    # return ranges sorted by start position
    return sorted(function_ranges, key=lambda x: x[0])


def extract_functions(
    input_filename: str,
    output_filename: str,
    include_directives: bool,
    include_calls: bool,
    *function_names: str
) -> None:
    """
    Extract the desired function names from the input file into the output file
    """

    unit = parse_file(input_filename)
    function_ranges = get_function_ranges(
        unit.cursor, include_calls, *function_names
    )

    contents = []
    with open(input_filename, "r") as input_file:
        if include_directives:
            for offset in get_direct_include_offsets(unit):
                # add inclusion directive to content to be written
                input_file.seek(offset)
                contents.append("#include " + input_file.readline().strip())

        for offset, length in get_global_ranges(unit.cursor):
            input_file.seek(offset)
            contents.append(input_file.read(length) + ";")

        for offset, length in function_ranges:
            # add function to content to be written
            input_file.seek(offset)
            contents.append(input_file.read(length))

    with open(output_filename, "w") as output_file:
        output_file.write("\n".join(contents))


def remove_functions(
    input_filename: str, output_filename: str, *function_names: str
) -> None:
    """
    Remove specified functions from the input file and write the result to the
    output file. This version uses adjusted token boundaries to ensure the
    entire function (including its declaration keyword) is removed.
    """
    # Parse the file and get the function ranges to remove.
    unit = parse_file(input_filename)
    found_functions = find_entities(
        unit.cursor,
        False,
        *((CursorKind.FUNCTION_DECL, func) for func in function_names)
    )

    # Read the entire file content.
    with open(input_filename, "r") as f:
        content = f.read()

    # Compute the ranges using the file content.
    function_ranges = [
        get_cursor_range(func, content) for func in found_functions
    ]

    # Remove each function by slicing out its range.
    # Removing in reverse order avoids shifting offsets.
    for offset, length in sorted(
        function_ranges, key=lambda r: r[0], reverse=True
    ):
        content = content[:offset] + content[offset + length :]

    # Write the modified content to the output file.
    with open(output_filename, "w") as f:
        f.write(content)
