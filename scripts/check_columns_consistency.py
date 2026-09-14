"""
SkyMetrics - Column Consistency Check
----------------------------------------
Checks whether all files in data/raw/ have identical columns.
If BTS's field selection didn't persist consistently across your 36
downloads, some files may have different columns than others - this
would break Power Query's "Append/Combine" step later, so it's
important to catch now.

Run:
    python check_columns_consistency.py
"""

import os
import glob
import pandas as pd

DATA_DIR = "data/raw"


def main():
    pattern = os.path.join(DATA_DIR, "*.csv")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No CSV files found in '{DATA_DIR}'.")
        return

    print(f"Checking column consistency across {len(files)} file(s)...\n")

    column_sets = {}  # frozenset of columns -> list of filenames

    for filepath in files:
        filename = os.path.basename(filepath)
        # Only read the header row - fast, no need to load full file
        df = pd.read_csv(filepath, nrows=0)
        cols = frozenset(df.columns)
        column_sets.setdefault(cols, []).append(filename)

    if len(column_sets) == 1:
        print("All files have IDENTICAL columns. Safe to combine.\n")
        cols = list(column_sets.keys())[0]
        print(f"Columns ({len(cols)} total):")
        for col in sorted(cols):
            print(f"  {col}")
    else:
        print(f"WARNING: Found {len(column_sets)} DIFFERENT column sets across your files.\n")
        for i, (cols, filenames) in enumerate(column_sets.items(), start=1):
            print(f"--- Column set {i} (used by {len(filenames)} file(s)) ---")
            print(f"Files: {', '.join(filenames)}")
            print(f"Columns: {sorted(cols)}\n")

        # Show the actual differences between the two most common sets, if exactly 2
        if len(column_sets) == 2:
            sets = list(column_sets.keys())
            only_in_1 = sets[0] - sets[1]
            only_in_2 = sets[1] - sets[0]
            print("DIFFERENCES:")
            if only_in_1:
                print(f"  Only in set 1: {sorted(only_in_1)}")
            if only_in_2:
                print(f"  Only in set 2: {sorted(only_in_2)}")


if __name__ == "__main__":
    main()