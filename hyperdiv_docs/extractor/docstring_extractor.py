def extract_docstring(source_lines, start_line):
    """
    Walks backward from start_line, collecting either the contents of a
    multi-line string, or the contents of a possibly multi-line
    '#' comment block. In the latter case, the comment block has
    to be contiguous, with each line starting with '#'. If it
    encounters a blank line, the comment stops there.
    """
    comment_lines = []

    inside_multiline_comment = False
    end_char = None  # Expected end char for a multi-line comment ('"""' or "'''")

    while start_line >= 0:
        line = source_lines[start_line]

        if inside_multiline_comment:
            if line.strip().startswith(end_char):
                # We encountered the start of a triple-quote
                # multi-line string. We append the chunk after the
                # triple-quotes.
                comment_lines.append(line[line.find(end_char) + len(end_char) :])
                break
            else:
                # We are inside a multi-line triple-quote
                # string. We append the line verbatim.
                comment_lines.append(line)

        else:
            stripped_line = line.strip()

            if stripped_line == '"""' or stripped_line == "'''":
                # We encountered the end of a multi-line
                # triple-quote string, where the final
                # triple-quote is on a line by itself.
                inside_multiline_comment = True
                end_char = stripped_line
            elif stripped_line.endswith('"""') or stripped_line.endswith("'''"):
                # We encountered the end of a multi-line string
                # that has content before the ending triple-quote.
                end_char = '"""' if stripped_line.endswith('"""') else "'''"

                if stripped_line.startswith(end_char):
                    # In this case, we have a triple-quote string
                    # that starts and ends on the same line.
                    line = line[
                        line.find(end_char) + len(end_char) : line.rfind(end_char)
                    ]

                    if line.strip() != "":
                        comment_lines.append(line)
                    break
                else:
                    # We encountered the end line of a multi-line
                    # triple-quote string. We append the content
                    # before the triple-quote.
                    inside_multiline_comment = True
                    comment_lines.append(line[: line.rfind(end_char)])
            elif stripped_line.startswith("#"):
                # A normal comment line.
                comment_lines.append(line[line.find("#") + 1 :])
            else:
                break

        start_line -= 1

    docstring = "\n".join(reversed(comment_lines))
    return docstring
