"""
SkyMetrics - Data Check Script (v2 - matches actual BTS prezipped column names)
--------------------------------------------------------------------------------
Run from inside your skymetrics project folder:
    python check_data.py

Requires: pandas
    pip install pandas
"""

import os
import glob
import pandas as pd

DATA_DIR = "data/raw"

# Actual column names as they appear in the BTS prezipped export
KEY_COLUMNS = [
    "DEP_DELAY", "ARR_DELAY", "CARRIER_DELAY", "WEATHER_DELAY",
    "NAS_DELAY", "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY",
    "CANCELLED", "CANCELLATION_CODE"
]


def check_file(filepath):
    filename = os.path.basename(filepath)
    expected_label = filename.replace(".csv", "")

    try:
        expected_year, expected_month = expected_label.split("_")
        expected_year = int(expected_year)
        expected_month = int(expected_month)
    except ValueError:
        expected_year, expected_month = None, None
        print(f"  [WARN] Could not parse expected year/month from filename '{filename}'")

    df = pd.read_csv(filepath, low_memory=False)
    row_count = len(df)

    year_ok = month_ok = "N/A"
    if "YEAR" in df.columns and expected_year is not None:
        actual_years = df["YEAR"].unique()
        year_ok = "OK" if list(actual_years) == [expected_year] else f"MISMATCH {actual_years}"

    if "MONTH" in df.columns and expected_month is not None:
        actual_months = df["MONTH"].unique()
        month_ok = "OK" if list(actual_months) == [expected_month] else f"MISMATCH {actual_months}"

    null_summary = {}
    for col in KEY_COLUMNS:
        if col in df.columns:
            null_summary[col] = int(df[col].isna().sum())

    return {
        "file": filename,
        "rows": row_count,
        "year_check": year_ok,
        "month_check": month_ok,
        "nulls": null_summary,
    }


def main():
    pattern = os.path.join(DATA_DIR, "*.csv")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No CSV files found in '{DATA_DIR}'.")
        return

    print(f"Found {len(files)} CSV file(s) in '{DATA_DIR}'\n")
    print(f"{'File':<16} {'Rows':>10}  {'Year Check':<14} {'Month Check':<14}")
    print("-" * 60)

    total_rows = 0
    results = []

    for filepath in files:
        result = check_file(filepath)
        results.append(result)
        total_rows += result["rows"]
        print(f"{result['file']:<16} {result['rows']:>10,}  {result['year_check']:<14} {result['month_check']:<14}")

    print("-" * 60)
    print(f"{'TOTAL':<16} {total_rows:>10,}")

    print("\nNull counts in key columns (summed across all files):")
    combined_nulls = {}
    for result in results:
        for col, count in result["nulls"].items():
            combined_nulls[col] = combined_nulls.get(col, 0) + count

    for col, count in combined_nulls.items():
        pct = (count / total_rows * 100) if total_rows else 0
        print(f"  {col:<20}: {count:>10,}  ({pct:.1f}%)")

    print(f"\nExpected 36 files for 2023-2025. You have {len(files)}.")
    if len(files) < 36:
        print(f"Still missing {36 - len(files)} file(s).")


if __name__ == "__main__":
    main()