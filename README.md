# Data_driven_stock_analysis

A complete end-to-end data engineering and analytics project designed to analyze one year of Nifty 50 stock performance using Python, Pandas, SQL, Streamlit, and Power BI.

# 🚀 Project Overview

This project focuses on performing deep stock analysis using daily price data (open, high, low, close, volume) for Nifty 50 stocks over 12 months.
It includes:

---->Automated YAML → CSV data extraction

---->Consolidated master stock dataset

---->Advanced financial calculations

---->SQL database storage with clean schema

---->Power BI dashboard with interactive insights

---->Streamlit web app for real-time exploration

# 🧠 Skills Demonstrated

---->Python (Pandas, NumPy)

---->SQL (MySQL using SQLAlchemy & PyMySQL)

---->Power BI Visualization

---->Streamlit Web Application

---->Data Cleaning & Transformation

---->Exploratory Data Analysis (EDA)

---->Statistical Metrics (Volatility, Daily Return, Cumulative Return)

---->Data Engineering (ETL)

# 📂 Project Structure

.
# 🛠️ Tech Stack
Component	Used For
Python	ETL, preprocessing, metrics computation
Pandas	Data cleaning, feature engineering
MySQL	Storing processed stock data
SQLAlchemy + PyMySQL	Python–SQL integration
Power BI	Visual dashboards
Streamlit	Interactive web interface
YAML	Raw dataset format

# 📥 Data Extraction (YAML → CSV)

YAML files are provided month-wise.

Script: etl_yaml_to_csv.py

Tasks performed:

---->Read all YAML files

---->Extract each stock entry

---->Build a prices_master.csv (all records combined)

---->Create symbols_master.csv based on metadata

# 📈 Financial Metrics Computed

Script: compute_metrics.py

🔹 Daily Returns

🔹 Yearly Return

🔹 Volatility (STD of daily returns)

🔹 Cumulative Return (1-year running growth)

🔹 Green vs Red Stock Count

🔹 Sector Performance (Average yearly return by sector)

🔹 Correlation Matrix (close price correlation)

🔹 Monthly Movers

🔹 Top 5 gainers & losers for each month.

# 🗄️ SQL Database Schema

Database: stockdb

symbols
column	type
symbol	VARCHAR
company	VARCHAR
sector	VARCHAR
prices
column	type
trade_date	DATE
symbol	VARCHAR
open_price	DECIMAL
high_price	DECIMAL
low_price	DECIMAL
close_price	DECIMAL
volume	BIGINT

# 📊 Power BI Dashboard Visuals

✔ 1. Sector-Wise Average Yearly Return (Bar Chart)

✔ 2. Volatility vs Yearly Return (Scatter Chart)

✔ 3. Cumulative Return of Top 5 Stocks (Line Chart)

✔ 4. Market Summary KPIs

---->Green stocks

---->Red stocks

---->Avg price

---->Avg volume

✔ 5. Top 10 Gainers (Bar Chart)


✔ 6. Top 10 Losers (Bar Chart)

✔ 7. Stock Correlation Heatmap (Matrix)

✔ 8. Monthly Movers — Top 5 Gainers & Losers (Column Chart)

# 🌐 Streamlit App

Features:

---->Stock filtering

---->Price trends

---->Cumulative returns

---->Volatility check

---->Sector-based insights

# 📦 Outputs

All final analysis outputs stored in folder DATA

Includes:

---->metrics_per_symbol.csv

---->top10_gainers.csv

---->top10_losers.csv

---->top10_volatility.csv

---->cumulative_returns.csv

---->sector_performance.csv

---->close_corr_matrix.csv

---->monthly_movers_top5_bottom5.csv

# 🏁 Conclusion

This project delivers a fully-built end-to-end stock analysis system combining:

---->ETL

---->Database management

---->Financial computation

---->Dashboarding

---->Interactive exploration


# 👨‍💻 Developer
 
  Nirudeeswar R
 
 📍 Chennai
 
 🎓 B.Tech CSE
 
 📧 nirudeeswarr14@gmail.com
