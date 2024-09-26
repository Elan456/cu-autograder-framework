"""
This file contains functions to parse and use entities from C and C++ files
"""

from clang.cindex import CursorKind, Index, Cursor


def find_entity(node: Cursor, kind: CursorKind, name: str) -> Cursor:
    """
    Recursively find the desired entity as a Cursor from the supplied node
    """

    if node.kind == kind and node.spelling == name:
        # found node!
        return node

    for child in node.get_children():
        entity = find_entity(child, kind, name)

        if entity is not None:
            return entity

    return None


def get_cursor_range(cursor: Cursor) -> tuple[int, int]:
    """
    Returns offset position and length of a Cursor in the source file
    """

    start = cursor.extent.start.offset
    end = cursor.extent.end.offset

    return (start, end - start)


def get_function_ranges(input_filename: str, output_filename: str,
                        function_names: tuple[str, ...]) -> list[tuple[int,
                                                                       int]]:
    """
    Get the ranges
    """

    # init Index to parse file and get TranslationUnit
    index = Index.create()
    tu = index.parse(input_filename)

    # store entity ranges for requested functions (if found)
    entity_ranges = []
    for func_name in function_names:
        entity = find_entity(tu.cursor, CursorKind.FUNCTION_DECL, func_name)
        if entity is not None:
            entity_ranges.append(get_cursor_range(entity))

    # return ranges sorted by start position
    return sorted(entity_ranges, key=lambda x: x[0])


def extract_functions(input_filename: str, output_filename: str,
                      *function_names: str) -> None:
    """
    Extract the desired function names from the input file into the output file
    """

    function_ranges = get_function_ranges(input_filename, output_filename,
                                          function_names)

    contents = []
    with open(input_filename, 'r') as input_file:
        for (offset, length) in function_ranges:
            # add function to content to write
            input_file.seek(offset)
            contents.append(input_file.read(length))

    with open(output_filename, 'w') as output_file:
        output_file.write('\n\n'.join(contents))


def remove_functions(input_filename: str, output_filename: str,
                     *function_names: str) -> None:
    """
    Remove specified function names from the input file and place in the output
    file
    """

    function_ranges = get_function_ranges(input_filename, output_filename,
                                          function_names)

    contents = []
    with open(input_filename, 'r') as input_file:
        prev_pos = 0
        for (offset, length) in function_ranges:
            # add file contents excluding function to remove
            contents.append(input_file.read(offset - prev_pos))
            input_file.seek(offset + length)

            # store new start position (end of removed function)
            prev_pos = offset + length

        # finish reading file contents
        contents.append(input_file.read())

    with open(output_filename, 'w') as output_file:
        output_file.write(''.join(contents))
