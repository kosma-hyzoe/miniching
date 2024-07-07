import sys

from datetime import datetime

from miniching import config as rc
from miniching.reference import REFERENCE


def get_result(hexagram, ascii_hex=False) -> str:
    result = f"{hexagram.origin}"

    if hexagram.lines:
        result += f":{','.join(hexagram.lines)} -> {hexagram.trans}"

        if hexagram.zhu_xi_eval and len(hexagram.lines) in [4, 5]:
            l_to_read = get_line_to_read_4_or_5_changing_lines(hexagram.lines)
            result += f"(:{l_to_read})"
        if ascii_hex:
            result += f" : {REFERENCE[hexagram.origin]['sign']} ->" \
                f" {REFERENCE[hexagram.trans]['sign']}"

    elif ascii_hex:
        result += f" : {REFERENCE[hexagram.origin]['sign']}"

    return result


def get_line_to_read_4_or_5_changing_lines(lines) -> str:
    opposite_lines = [str(l) for l in range(1, 7) if str(l) not in lines]
    return opposite_lines[0]


def format_hexagram_title(title) -> str:
    if "(" in title:
        title = title[:title.index("(") - 1]
    elif "[" in title:
        title = title[:title.index("[") - 1]
    return title
