import pandas as pd
from pathlib import Path

# Input and output files
SECTOR_CSV = "sector_mapping.csv"
INTERIM_PRICES = "data/interim/prices_all.csv"
OUT_MASTER = "data/interim/prices_master.csv"
OUT_SYMBOLS = "data/interim/symbols_master.csv"

def normalize_sector_file(path=SECTOR_CSV):
    df = pd.read_csv(path)
    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # Extract ticker from 'symbol' column like "ASIAN PAINTS: ASIANPAINT"
    def get_ticker(s):
        if pd.isna(s): return None
        parts = str(s).split(":")
        return parts[-1].strip().upper() if len(parts) >= 2 else str(s).strip().upper()
    df["symbol"] = df["symbol"].apply(get_ticker)
    df["company"] = df["company"].str.strip()
    df["sector"] = df["sector"].str.strip().str.upper()
    return df[["symbol","company","sector"]].dropna().drop_duplicates()

def main():
    Path("data/interim").mkdir(parents=True, exist_ok=True)
    # Load and clean sector data
    sym = normalize_sector_file()
    sym.sort_values("symbol").to_csv(OUT_SYMBOLS, index=False)

    # Load stock price data
    prices = pd.read_csv(INTERIM_PRICES, parse_dates=["trade_date"])
    prices["symbol"] = prices["symbol"].str.upper()
    prices["volume"] = prices["volume"].clip(lower=0)
    prices.to_csv(OUT_MASTER, index=False)

    print(f"✅ Cleaned prices saved to: {OUT_MASTER}")
    print(f"✅ Sector-symbol mapping saved to: {OUT_SYMBOLS}")

if __name__ == "__main__":
    main()
