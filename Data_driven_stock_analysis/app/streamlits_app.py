import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==================================
# 🎛️ PAGE CONFIG
# ==================================
st.set_page_config(page_title="📊 Nifty 50 Stock Analysis", layout="wide")

DATA_DIR = "data/processed"

# ==================================
# 🧠 LOAD DATA
# ==================================
@st.cache_data
def load_data():
    top10 = pd.read_csv(f"{DATA_DIR}/top10_gainers.csv")
    bot10 = pd.read_csv(f"{DATA_DIR}/top10_losers.csv")
    vol   = pd.read_csv(f"{DATA_DIR}/top10_volatility.csv")
    cum   = pd.read_csv(f"{DATA_DIR}/cumulative_returns.csv", parse_dates=["trade_date"])
    msum  = pd.read_csv(f"{DATA_DIR}/market_summary.csv").iloc[0].to_dict()
    sector= pd.read_csv(f"{DATA_DIR}/sector_performance.csv")
    corr  = pd.read_csv(f"{DATA_DIR}/close_corr_matrix.csv", index_col=0)
    movers= pd.read_csv(f"{DATA_DIR}/monthly_movers_top5_bottom5.csv")
    return top10, bot10, vol, cum, msum, sector, corr, movers

top10, bot10, vol, cum, msum, sector, corr, movers = load_data()

# ==================================
# 🏠 HEADER
# ==================================
st.title("📈 Nifty 50 Stock Performance Dashboard")

# ==================================
# 💡 MARKET SUMMARY
# ==================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Green Stocks", int(msum["green_count"]))
col2.metric("Red Stocks", int(msum["red_count"]))
col3.metric("Average Price", f"₹{msum['avg_price']:.2f}")
col4.metric("Average Volume", f"{msum['avg_volume']:.0f}")

st.markdown("---")

# ==================================
# 🥇 TOP 10 GAINERS & LOSERS
# ==================================
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 Gainers")
    st.bar_chart(top10.set_index("symbol")["yearly_return"])

with col2:
    st.subheader("Top 10 Losers")
    st.bar_chart(bot10.set_index("symbol")["yearly_return"])

st.markdown("---")

# ==================================
# ⚡ VOLATILITY
# ==================================
st.subheader("Top 10 Most Volatile Stocks")
st.bar_chart(vol.set_index("symbol")["volatility"])

st.markdown("---")

# ==================================
# 📈 CUMULATIVE RETURNS
# ==================================
st.subheader("Cumulative Return Over Time (Top 5 Performing Stocks)")

# Find top 5 symbols by latest cumulative return
latest_cum = cum.groupby("symbol")["cumret"].last().nlargest(5).index
fig, ax = plt.subplots(figsize=(10, 5))
for sym in latest_cum:
    subset = cum[cum["symbol"] == sym]
    ax.plot(subset["trade_date"], subset["cumret"], label=sym)
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.set_title("Top 5 Performing Stocks")
st.pyplot(fig)

st.markdown("---")

# ==================================
# 🏭 SECTOR PERFORMANCE
# ==================================
st.subheader("Average Yearly Return by Sector")
st.bar_chart(sector.set_index("sector")["yearly_return"])

st.markdown("---")

# ==================================
# 🔥 CORRELATION HEATMAP
# ==================================
st.subheader("Stock Price Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("---")

# ==================================
# 📅 MONTHLY MOVERS
# ==================================
st.subheader("Top 5 Gainers and Losers by Month")

month_choice = st.selectbox("Select Month", sorted(movers["month"].unique()))
view = movers[movers["month"] == month_choice]

col1, col2 = st.columns(2)
col1.write("**Top 5 Gainers**")
col1.dataframe(view[view["direction"] == "gainer"][["symbol", "monthly_return"]])

col2.write("**Top 5 Losers**")
col2.dataframe(view[view["direction"] == "loser"][["symbol", "monthly_return"]])
