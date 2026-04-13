"""Combine daily sales CSVs into pink morsel rows with Sales, Date, Region."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
INPUT_FILES = [
    DATA_DIR / "daily_sales_data_0.csv",
    DATA_DIR / "daily_sales_data_1.csv",
    DATA_DIR / "daily_sales_data_2.csv",
]
OUTPUT_PATH = DATA_DIR / "pink_morsel_sales.csv"


def main() -> None:
    frames = [pd.read_csv(path) for path in INPUT_FILES]
    df = pd.concat(frames, ignore_index=True)

    pink = df[df["product"].str.lower().str.strip() == "pink morsel"].copy()
    price = (
        pink["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .pipe(pd.to_numeric)
    )
    pink["Sales"] = pink["quantity"] * price
    pink["Date"] = pink["date"]
    pink["Region"] = pink["region"]

    out = pink[["Sales", "Date", "Region"]].sort_values(
        ["Date", "Region"], kind="mergesort"
    )
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(out)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
