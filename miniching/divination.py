import random

from miniching.serialization import BINARY_TO_DECIMAL


def get_excerpt_with_yarrow_stalks() -> str:
    pass


def get_excerpt_with_coin_toss() -> str:
    changing_lines = []
    reversed_hex_binary = []

    for line in range(1, 7):
        coin_throw_sum = random.choice([2, 3]) + random.choice([2, 3]) + random.choice([2, 3])
        reversed_hex_binary.append(0) if coin_throw_sum % 2 == 0 else reversed_hex_binary.append(1)
        if coin_throw_sum == 6 or coin_throw_sum == 9:
            changing_lines.append(line)

    hex_binary_representation = "".join(str(line) for line in reversed_hex_binary[::-1])
    hex_decimal = BINARY_TO_DECIMAL[hex_binary_representation]
    if changing_lines:
        changing_lines_representation = ",".join(str(line) for line in changing_lines)
        return f"{hex_decimal}:{changing_lines_representation}"
    else:
        return str(hex_decimal)






