import os
import glob
import yaml
import pandas as pd
from pathlib import Path

# =========================
# 📁 Directories
# =========================
RAW_DIR = "data/raw_yaml"
INTERIM_DIR = "data/interim"
PROCESSED_DIR = "data/processed"

Path(INTERIM_DIR).mkdir(parents=True, exist_ok=True)
Path(PROCESSED_DIR).mkdir(parents=True, exist_ok=True)

# =========================
# 🧠 Helper to read YAML safely
# =========================
def load_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️ Error reading {path}: {e}")
        return None

# =========================
# 🚀 Main Extraction Function
# =========================
def main():
    rows = []
    yaml_files = glob.glob(os.path.join(RAW_DIR, "**", "*.yaml"), recursive=True)
    print(f"📂 Found {len(yaml_files)} YAML files under {RAW_DIR}")

    for file in yaml_files:
        data = load_yaml(file)
        if not data or not isinstance(data, list):
            continue  # skip empty or invalid files

        for entry in data:
            try:
                rows.append({
                    "trade_date": pd.to_datetime(entry.get("date")).date(),
                    "symbol": str(entry.get("Ticker", "")).strip().upper(),
                    "open": float(entry.get("open", 0)),
                    "high": float(entry.get("high", 0)),
                    "low": float(entry.get("low", 0)),
                    "close": float(entry.get("close", 0)),
                    "volume": int(entry.get("volume", 0))
                })
            except Exception as e:
                print(f"⚠️ Skipping record in {file}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    if df.empty:
        print("⚠️ No data extracted! Please check YAML content again.")
        return

    df = df.sort_values(["symbol", "trade_date"]).reset_index(drop=True)

    # =========================
    # 💾 Save combined CSV
    # =========================
    combined_path = os.path.join(INTERIM_DIR, "prices_all.csv")
    df.to_csv(combined_path, index=False)
    print(f"✅ Combined data saved to: {combined_path}")

    # =========================
    # 💾 Split each symbol into its own CSV
    # =========================
    for symbol, group in df.groupby("symbol"):
        out_path = os.path.join(PROCESSED_DIR, f"{symbol}.csv")
        group.to_csv(out_path, index=False)

    print(f"✅ Created {df['symbol'].nunique()} symbol files in: {PROCESSED_DIR}")

# =========================
# 🏁 Entry point
# =========================
if __name__ == "__main__":
    main()
