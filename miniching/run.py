import os
import sys
import argparse
import datetime

from miniching import hexagrams
from miniching import config as rc
from miniching.reading.compose import compose_reading
from miniching.reading.helpers import get_result
from miniching.reading.reading import get_full_reading

H_ZHU_XI = \
    "use the modified Zhu Xi evaluation method instead of the classic " \
    "'read all changing lines' method"
H_READING = \
    "get full reading, not just the 'hex:lines -> hex' style result"
H_SKIP_HISTORY = \
    "don't write to history, even if -p flag was provided"
H_QUERY = \
    "provide a query instead of the default prompt or posix redirects"
H_EXCERPT = \
    "provide an excerpt using the '64' /'61:1,2' format" \
    "or the 3 coin sum notation where '788688' -> 23:3"
H_TIMESTAMP = \
    "provide a timestamp, any format"
H_HISTORY_PATH = \
    "provide an alternative history path, file or directory path"
H_ASCII_HEX = \
    "use ascii symbols to mirror the hexagram next to their numbers"
H_PRINT_LAST = \
    "print the last history record, can be combined with -r and -p." \
    "will ignore -t, -e and -q flags"

E_PATH = "Error: Invalid history file path"
E_NO_HISTORY = "Error: No history file at"
E_CORRUPTED_HISTORY = "Error: History file corrupted at path"


def run():
    args = _get_parser_args()

    path = _get_history_path(args.history_path)
    if args.l__print_last:
        args.timestamp, args.query, args.excerpt, args.zhu_xi = read_last(path)

    hexagram = \
        hexagrams.get_from_excerpt(args.excerpt, args.zhu_xi) if args.excerpt \
        else hexagrams.get_with_coin_toss(args.zhu_xi)
    timestamp = \
        args.timestamp if args.timestamp \
        else datetime.datetime.now().strftime(rc.TIMESTAMP_FORMAT)
    query = \
        args.query if args.query \
        else input("Query: ")
    reading = compose_reading(hexagram, timestamp, query)

    result = get_result(hexagram, ascii_hex=args.asci_hex)
    if args.l__print_last:
        print(args.timestamp)
        print(args.query)
    print(get_full_reading(reading, result)) if args.reading else print(result)

    if not args.skip_history and not args.l__print_last:
        write_history(reading, result, path)


def write_history(reading, result, path):
    with open(path, "a+") as f:
        f.write(reading.timestamp + rc.LINE_BREAK)
        f.write(reading.query + rc.LINE_BREAK)
        f.write(result + rc.LINE_BREAK)

        f.write(rc.LINE_BREAK)


def read_last(path):
    if not os.path.exists(path):
        print(E_NO_HISTORY, path, file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except IsADirectoryError:
        path = os.path.join(path, rc.HISTORY_FILENAME)
    except OSError:
        print(E_PATH, path, file=sys.stderr)
        sys.exit(1)

    try:
        timestamp = lines[-4].strip()
        query = lines[-3].strip()
        result = lines[-2].strip()
    except IndexError:
        print(E_CORRUPTED_HISTORY, path, file=sys.stderr)
        exit(1)

    zhu_xi_eval = "(" in result
    excerpt = result[:result.index(" ")] if " " in result else result

    return timestamp, query, excerpt, zhu_xi_eval


def _get_history_path(path):
    if not path:
        path = os.path.join(rc.DEFAULT_HISTORY_DIR, rc.HISTORY_FILENAME)

    try:
        with open(path, 'a+'):
            pass
    except IsADirectoryError:
        path = os.path.join(path, rc.HISTORY_FILENAME)
    except OSError:
        print(E_PATH, path, file=sys.stderr)
        sys.exit(1)
    return path


def _get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zhu-xi", action="store_true",
                        help=H_ZHU_XI)
    parser.add_argument("-r", "--reading", action="store_true",
                        help=H_READING)
    parser.add_argument("-s", "--skip-history", action="store_true",
                        help=H_SKIP_HISTORY)
    parser.add_argument("-q", "--query", type=str, default=None,
                        help=H_QUERY)
    parser.add_argument("-e", "--excerpt", type=str, default=None,
                        help=H_EXCERPT)
    parser.add_argument("-t", "--timestamp", type=str, default=None,
                        help=H_TIMESTAMP)
    parser.add_argument("-p", "--history-path", type=str, default=None,
                        help=H_HISTORY_PATH)
    parser.add_argument("-a", "--asci-hex", action="store_true",
                        help=H_ASCII_HEX)
    parser.add_argument("-l" "--print-last", action="store_true",
                        help=H_PRINT_LAST)
    return parser.parse_args()
