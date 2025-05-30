"""
Parser file to parse most active cookie for a date
"""
import argparse
import csv
import logging
import os
import sys
from collections import Counter
from datetime import datetime, date
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# pylint: disable = line-too-long
def validate_date(date_str: str) ->date:
    """Validate and parse date in YYYY-MM-DD format."""
    logging.info("Validating date string: %s", date_str)
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError as e:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format (e.g., 2018-12-09)") from e


def validate_file(file_path: str) -> str:
    """Validate that file exists and is readable."""
    logging.info("Validating file path: %s", file_path)
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    if not os.access(file_path, os.R_OK):
        raise argparse.ArgumentTypeError(f"File '{file_path}' is not readable.")
    return file_path


def parse_cookie_log(file_path: str, target_date: date) -> List[str]:
    """Extract cookies that match the target date."""
    matching_cookies = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Skip the header
            if header != ["cookie", "timestamp"]:
                logging.warning("Unexpected header: %s", header)

            for line_num, row in enumerate(reader, start=2):  # start from line 2 due to header
                if len(row) != 2:
                    logging.warning("Skipping malformed row %s: %s", line_num, row)
                    continue

                cookie, timestamp = row
                timestamp = timestamp.strip().replace('Z', '+00:00')

                try:
                    log_date = datetime.fromisoformat(timestamp).date()
                    if log_date == target_date:
                        matching_cookies.append(cookie)
                except ValueError:
                    logging.error("Skipping invalid timestamp on row %s: %s", line_num, timestamp)
    except Exception as e:
        logging.error("Error reading file %s: %s", file_path, e)
        raise

    return matching_cookies


def find_most_active_cookies(cookies: List[str]) -> List[str]:
    """Find the most frequent cookies from the list."""
    logging.info("Finding most active cookies...")
    if not cookies:
        return []

    counter = Counter(cookies)
    max_count = max(counter.values())
    return [cookie for cookie, count in counter.items() if count == max_count]


# pylint: disable = broad-exception-caught
def main():
    """
    Main entry point.
    :return:
    """
    parser = argparse.ArgumentParser(description="Find the most active cookies for a given date.")
    parser.add_argument("-f", "--file", type=validate_file, required=True, help="Path to the cookie log CSV file.")
    parser.add_argument("-d", "--date", type=validate_date, required=True, help="Date to filter cookies (YYYY-MM-DD).")

    args = parser.parse_args()

    logging.info("Processing file: %s for date: %s", args.file, args.date)
    try:
        cookies = parse_cookie_log(args.file, args.date)
        most_active = find_most_active_cookies(cookies)

        if most_active:
            logging.info("Most active cookie(s):")
            for cookie in most_active:
                print(cookie)
        else:
            logging.info("No cookies found for the given date.")
    except Exception:
        logging.exception("An unexpected error occurred.")
        sys.exit(1)


if __name__ == "__main__":
    main()
