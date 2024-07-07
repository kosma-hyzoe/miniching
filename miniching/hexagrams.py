import re
import sys
from random import choice

from miniching.reading.models import Hexagram
from miniching.reference import DECIMAL_TO_BINARY, BINARY_TO_DECIMAL

E_EXCERPT = \
    "Invalid excerpt format.\n" \
    "Use '23'/ '23:3' format or 3-coin sum notation ('788688' -> 23:3)"


def get_with_coin_toss(zhu_xi_eval: bool) -> Hexagram:
    changing_lines: list[str] = []
    origin_binary: list[str] = []
    trans_binary: list[str] = []

    # Six 3-coin tosses are emulated. 0/1s are added to the hexagrams' binary
    # representation.  Note that i.e. '000111'(11: "Peace"), the first character
    # corresponds to line 6 and last character to line 1 – I don't like it, but
    # this seems to be a common convention among I-Ching apps. The numbers of
    # changing lines are appended along the way.
    for line in range(1, 7):
        coin_sum = choice([2, 3]) + choice([2, 3]) + choice([2, 3])
        if coin_sum == 7:
            origin_binary.insert(0, "1")
            trans_binary.insert(0, "1")
        elif coin_sum == 8:
            origin_binary.insert(0, "0")
            trans_binary.insert(0, "0")
        elif coin_sum == 9:
            origin_binary.insert(0, "1")
            trans_binary.insert(0, "0")
            changing_lines.append(str(line))
        elif coin_sum == 6:
            origin_binary.insert(0, "0")
            trans_binary.insert(0, "1")
            changing_lines.append(str(line))

    origin_decimal = BINARY_TO_DECIMAL["".join(origin_binary)]
    trans_decimal = BINARY_TO_DECIMAL["".join(trans_binary)]
    return Hexagram(origin_decimal, trans_decimal, changing_lines, zhu_xi_eval)


def get_from_excerpt(excerpt: str, classic_eval: bool) -> Hexagram:
    if re.match(r"^\d{1,2}$", excerpt):
        origin = excerpt
        trans = None
        changing_lines = []
    elif re.match(r"^\d{1,2}:(\d,){0,5}\d$", excerpt):
        origin = excerpt[: excerpt.index(":")]
        if int(origin) not in range(1, 65):
            print(E_EXCERPT, file=sys.stderr)
            sys.exit(1)
        changing_lines = excerpt[excerpt.index(":") + 1:].split(",")
        origin_binary = [line_value for line_value in DECIMAL_TO_BINARY[origin]]
        trans_binary = []
        zip_lines = zip([str(line) for line in range(6, 0, -1)], origin_binary)

        for line, line_value in zip_lines:
            opposite_line_value = "1" if line_value == "0" else "0"
            if line in changing_lines:
                trans_binary.append(opposite_line_value)
            else:
                trans_binary.append(line_value)
        trans = BINARY_TO_DECIMAL["".join(trans_binary)]
    elif re.match(r"^[6789]{6}$", excerpt):
        origin_binary = []
        trans_binary = []
        changing_lines = []
        tmp_lines = [str(line) for line in range(6, 0, -1)]
        for coin_sum, line_number in zip(excerpt, tmp_lines):
            if coin_sum == "7":
                origin_binary.append("1")
                trans_binary.append("1")
            elif coin_sum == "8":
                origin_binary.append("0")
                trans_binary.append("0")
            elif coin_sum == "9":
                origin_binary.append("1")
                trans_binary.append("0")
                changing_lines.append(line_number)
            elif coin_sum == "6":
                origin_binary.append("0")
                trans_binary.append("1")
                changing_lines.append(line_number)

        origin = BINARY_TO_DECIMAL["".join(origin_binary)]
        trans = BINARY_TO_DECIMAL["".join(trans_binary)]
    else:
        print(E_EXCERPT, file=sys.stderr)
        sys.exit(1)
    return Hexagram(origin, trans, changing_lines, classic_eval)
