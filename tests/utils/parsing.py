"""
This file contains functions to parse and use entities from C and C++ files
"""

from clang.cindex import Cursor, CursorKind, Index, TranslationUnit


def find_entities(node: Cursor, include_calls: bool,
                  *entities: tuple[CursorKind, str]) -> list[Cursor, ...]:
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
            if any(child.kind == kind and child.spelling == name for
                   kind, name in entities):
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
                if str(child.location.file) == str(current_entity.location.
                                                   file):
                    # check if child is call expression to ref in same file
                    if child.kind == CursorKind.CALL_EXPR and \
                            child.referenced is not None and \
                            str(child.referenced.location.file) == str(
                                current_entity.location.file) \
                            and child.referenced not in found_entities:
                        # add call expression's reference if true
                        found_entities.append(child.referenced)
                        stack.append(child.referenced)
                    else:
                        stack.append(child)

    return found_entities


def get_direct_include_offsets(tu: TranslationUnit) -> tuple[int, ...]:
    """
    Returns the offsets for the inclusion directives directly in the file
    """

    return (x.location.offset for x in
            filter(lambda x: x.depth == 1,  # only direct includes
                   tu.get_includes()))


def get_cursor_range(cursor: Cursor) -> tuple[int, int]:
    """
    Returns offset position and length of a Cursor in the source file
    """

    start = cursor.extent.start.offset
    end = cursor.extent.end.offset

    return (start, end - start)


def parse_file(input_filename: str) -> TranslationUnit:
    """
    Return the TranslationUnit for the given file
    """

    # init Index to parse file
    index = Index.create()

    return index.parse(input_filename)


def get_function_ranges(cursor: Cursor, include_calls: bool,
                        *function_names: str) -> list[tuple[int, int]]:
    """
    Get the ranges for supplied functions
    """

    found_functions = find_entities(cursor, include_calls,
                                    *((CursorKind.FUNCTION_DECL, func)
                                      for func in function_names),
                                    )

    # store entity ranges for found requested functions
    function_ranges = map(get_cursor_range, found_functions)

    # return ranges sorted by start position
    return sorted(function_ranges, key=lambda x: x[0])


def extract_functions(input_filename: str, output_filename: str,
                      include_directives: bool, include_calls: bool,
                      *function_names: str) -> None:
    """
    Extract the desired function names from the input file into the output file
    """

    unit = parse_file(input_filename)
    function_ranges = get_function_ranges(unit.cursor, include_calls,
                                          *function_names)

    contents = []
    with open(input_filename, "r") as input_file:
        if include_directives:
            for offset in get_direct_include_offsets(unit):
                # add inclusion directive to content to be written
                input_file.seek(offset)
                contents.append('#include ' + input_file.readline().strip())

        for (offset, length) in function_ranges:
            # add function to content to be written
            input_file.seek(offset)
            contents.append(input_file.read(length))

    with open(output_filename, "w") as output_file:
        output_file.write("\n".join(contents))


def remove_functions(input_filename: str, output_filename: str,
                     *function_names: str) -> None:
    """
    Remove specified function names from the input file and place in the output
    file
    """

    unit = parse_file(input_filename)
    function_ranges = get_function_ranges(unit.cursor, False, *function_names)

    contents = []
    with open(input_filename, "r") as input_file:
        prev_pos = 0
        for (offset, length) in function_ranges:
            # add file contents excluding function to remove
            contents.append(input_file.read(offset - prev_pos))
            input_file.seek(offset + length)

            # store new start position (end of removed function)
            prev_pos = offset + length

        # finish reading file contents
        contents.append(input_file.read())

    with open(output_filename, "w") as output_file:
        output_file.write("".join(contents))
