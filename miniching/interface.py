import argparse
import sys
from datetime import datetime

from miniching.divination import get_excerpt_with_coin_toss, get_excerpt_with_yarrow_stalks
from miniching.serialization import write_history, get_config
from miniching.reading.compose import compose_reading
from miniching.reading.format import format_datetime, LINE_BREAK
from miniching.reading.parse import ReadingParser


def main():
    parser_args = get_parser_args()
    now = format_datetime(datetime.now())

    if parser_args.manual_timestamp:
        timestamp = parser_args.manual_timestamp
        check_timestamp(timestamp)
    else:
        timestamp = now

    if parser_args.quick:
        query = '...'
    else:
        query = input("Query: ")

    if parser_args.manual_excerpt:
        excerpt = parser_args.manual_excerpt
    elif parser_args.yarrow_stalks:
        excerpt = get_excerpt_with_yarrow_stalks()
    else:
        excerpt = get_excerpt_with_coin_toss()

    reading = compose_reading(excerpt, timestamp, query, parser_args.classic)
    reading_parser = ReadingParser(reading)

    if not parser_args.skip_print:
        parsed_reading = reading_parser.get_printable_reading(parser_args.full_reading)
        print(LINE_BREAK + parsed_reading, end="")
    if parser_args.write_history:
        parsed_reading = reading_parser.get_history_record()
        write_history(parsed_reading)


def check_timestamp(timestamp):
    try:
        datetime.strptime(timestamp, get_config().get("formats", "timestamp"))
    except ValueError as e:
        print("Error: " + str(e) + " provided in the config file.")
        sys.exit(1)


def get_parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--full-reading', action='store_true', help='get a full reading')
    parser.add_argument('-w', '--write-history', action='store_true', help='write to a history.txt file')
    parser.add_argument('-s', '--skip-print', action='store_true', help='don\'t print the reading')
    parser.add_argument('-y', '--yarrow-stalks', action='store_true', help='use the yarrow stalks divination method')

    parser.add_argument('-q', '--quick', action="store_true", help="get a reading with an empty query")

    classic_help = "use classic evaluation / 'read all changing lines' instead of the default modified Zhu Xi method"
    parser.add_argument('-c', '--classic', action='store_true', help=classic_help)
    manual_excerpt_help = "provide an excerpt using '64' format for pure hexes or '63:1,2' with changing lines"
    parser.add_argument('-e', '--manual-excerpt', type=str, default=None, help=manual_excerpt_help)
    manual_timestamp_help = "provide a timestamp matching the provided format (by default it's %%d-%%m-%%Y)"
    parser.add_argument('-t', '--manual-timestamp', type=str, default=None, help=manual_timestamp_help)

    return parser.parse_args()


if __name__ == "__main__":
    main()



























