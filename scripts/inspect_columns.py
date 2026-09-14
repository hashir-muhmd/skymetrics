import pandas as pd

df = pd.read_csv("data/raw/2023_01.csv", nrows=5, low_memory=False)
print("Column names found in file:\n")
for col in df.columns:
    print(f"  '{col}'")

print("\nFirst 2 rows preview:")
print(df.head(2).to_string())