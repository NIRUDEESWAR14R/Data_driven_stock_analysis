import pandas as pd
import numpy as np
import os

# ================================
# File Paths
# ================================
MASTER = "data/interim/prices_master.csv"
SYMS   = "data/interim/symbols_master.csv"
OUTDIR = "data/processed"

os.makedirs(OUTDIR, exist_ok=True)

# ================================
# Helper Functions
# ================================

def add_returns(df):
    """Add previous close and daily returns."""
    df = df.sort_values(["symbol","trade_date"]).copy()
    df["prev_close"] = df.groupby("symbol")["close"].shift(1)
    df["daily_ret"] = (df["close"] - df["prev_close"]) / df["prev_close"]
    return df


def yearly_returns(df):
    """Compute yearly return per symbol."""
    g = df.sort_values("trade_date").groupby("symbol")
    first = g["close"].first()
    last  = g["close"].last()
    return ((last/first - 1.0).rename("yearly_return").reset_index())


def volatility(df):
    """Standard deviation of daily returns per symbol."""
    return (
        df.groupby("symbol")["daily_ret"].std()
        .rename("volatility")
        .reset_index()
        .sort_values("volatility", ascending=False)
    )


def cumulative_returns(df):
    """Cumulative return over time per symbol."""
    df = df.sort_values(["symbol","trade_date"]).copy()
    df["cumret"] = df.groupby("symbol")["daily_ret"].transform(
        lambda r: (1 + r).cumprod() - 1
    )
    return df[["trade_date","symbol","cumret"]]


def market_summary(df):
    """Market-wide summary statistics."""
    yr = yearly_returns(df)
    return {
        "green_count": int((yr["yearly_return"]>0).sum()),
        "red_count":   int((yr["yearly_return"]<=0).sum()),
        "avg_price":   float(round(df["close"].mean(),2)),
        "avg_volume":  float(round(df["volume"].mean(),0))
    }


def sector_performance(yr, symbols):
    """Average return per sector."""
    return (
        yr.merge(symbols, on="symbol", how="left")
          .groupby("sector", dropna=False)["yearly_return"]
          .mean().reset_index()
          .sort_values("yearly_return", ascending=False)
    )


def correlation_matrix(df):
    """Correlation matrix of stock returns."""
    pv = df.pivot(index="trade_date", columns="symbol", values="close").sort_index()
    returns = pv.pct_change().dropna(how="all")
    return returns.corr()


def monthly_movers(df):
    """Top 5 gainers and losers each month."""
    df["month"] = df["trade_date"].dt.to_period("M")
    g = df.groupby(["symbol","month"])["close"]
    m = (g.last()/g.first()-1.0).rename("monthly_return").reset_index()

    top5 = (
        m.sort_values(["month","monthly_return"], ascending=[True, False])
         .groupby("month").head(5).assign(direction="gainer")
    )

    bottom5 = (
        m.sort_values(["month","monthly_return"], ascending=[True, True])
         .groupby("month").head(5).assign(direction="loser")
    )

    return pd.concat([top5,bottom5], ignore_index=True)


# ================================
# NEW: metrics_per_symbol for Power BI
# ================================

def compute_symbol_metrics(prices, symbols):
    """Create per-symbol metrics for Power BI visuals."""
    prices_sector = prices.merge(symbols, on="symbol", how="left")
    prices_sector = prices_sector.sort_values(["symbol", "trade_date"]).copy()

    # Ensure daily_ret exists
    if "daily_ret" not in prices_sector.columns:
        prices_sector["prev_close"] = prices_sector.groupby("symbol")["close"].shift(1)
        prices_sector["daily_ret"] = (
            prices_sector["close"] - prices_sector["prev_close"]
        ) / prices_sector["prev_close"]

    summary = (
        prices_sector
        .groupby(["symbol", "company", "sector"], as_index=False)
        .agg(
            first_open=("open", "first"),
            last_close=("close", "last"),
            avg_close=("close", "mean"),
            avg_volume=("volume", "mean"),
            volatility=("daily_ret", "std")
        )
    )

    summary["yearly_return"] = (
        (summary["last_close"] - summary["first_open"]) /
        summary["first_open"]
    )
    summary["volatility"] = summary["volatility"] * 100
    summary["yearly_return"] = summary["yearly_return"] * 100

    summary = summary[
        ["symbol", "company", "sector", "yearly_return",
         "volatility", "avg_close", "avg_volume"]
    ]

    return summary


# ================================
# Main Runner
# ================================

def run_all():
    print("🔄 Loading data...")
    prices = pd.read_csv(MASTER, parse_dates=["trade_date"])
    symbols = pd.read_csv(SYMS)

    print("📈 Computing daily returns...")
    prices = add_returns(prices)

    print("🏆 Top gainers & losers...")
    yr = yearly_returns(prices)
    vol_top10 = volatility(prices).head(10)
    cum = cumulative_returns(prices)
    msum = market_summary(prices)
    sect = sector_performance(yr, symbols)
    corr = correlation_matrix(prices)
    movers = monthly_movers(prices)

    # Save original project outputs
    yr.nlargest(10,"yearly_return").to_csv(f"{OUTDIR}/top10_gainers.csv", index=False)
    yr.nsmallest(10,"yearly_return").to_csv(f"{OUTDIR}/top10_losers.csv", index=False)
    vol_top10.to_csv(f"{OUTDIR}/top10_volatility.csv", index=False)
    cum.to_csv(f"{OUTDIR}/cumulative_returns.csv", index=False)
    pd.DataFrame([msum]).to_csv(f"{OUTDIR}/market_summary.csv", index=False)
    sect.to_csv(f"{OUTDIR}/sector_performance.csv", index=False)
    corr.to_csv(f"{OUTDIR}/close_corr_matrix.csv")
    movers.to_csv(f"{OUTDIR}/monthly_movers_top5_bottom5.csv", index=False)

    print("📊 Computing symbol-level metrics for Power BI...")
    summary = compute_symbol_metrics(prices, symbols)
    summary.to_csv(f"{OUTDIR}/metrics_per_symbol.csv", index=False)

    print("🎉 All metrics saved in data/processed")


if __name__ == "__main__":
    run_all()
