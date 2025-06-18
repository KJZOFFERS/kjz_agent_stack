import csv
import os
import sys

import gspread

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")


def parse_csv(path: str):
    """Return list of [Name, Phone, Email] rows from Propwire CSV."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        required = ["Name", "Phone", "Email"]
        for col in required:
            if col not in reader.fieldnames:
                raise ValueError(f"Missing column {col} in CSV")
        return [[row["Name"], row["Phone"], row["Email"]] for row in reader]


def append_rows(rows):
    """Append rows to the Google Sheet."""
    if not SHEET_ID:
        raise EnvironmentError("GOOGLE_SHEET_ID environment variable not set")
    gc = gspread.service_account()
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.sheet1
    worksheet.append_rows(rows, value_input_option="RAW")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python buyers_scraper.py path/to/propwire.csv")
        return 1
    csv_path = argv[0]
    rows = parse_csv(csv_path)
    if rows:
        append_rows(rows)
        print(f"Appended {len(rows)} rows to sheet {SHEET_ID}")
    else:
        print("No rows to append")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
