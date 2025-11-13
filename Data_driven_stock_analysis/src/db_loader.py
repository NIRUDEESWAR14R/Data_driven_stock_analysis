import os
import pandas as pd
from sqlalchemy import create_engine

# Read environment variable if .env exists, else use direct connection
DB_URL = os.getenv("SQLALCHEMY_URL", "mysql+pymysql://root:12345@localhost:3306/stockdb")

# Paths
SYMBOLS_CSV = "data/interim/symbols_master.csv"
PRICES_CSV  = "data/interim/prices_master.csv"

def main():
    print("Connecting to database...")
    engine = create_engine(DB_URL)

    # Load data
    symbols = pd.read_csv(SYMBOLS_CSV)
    prices = pd.read_csv(PRICES_CSV, parse_dates=["trade_date"])

    print("Uploading tables...")
    symbols.to_sql("symbols", engine, if_exists="replace", index=False)
    prices.to_sql("prices", engine, if_exists="replace", index=False)
    print("✅ Data successfully loaded into MySQL database!")

if __name__ == "__main__":
    main()
