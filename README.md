# market_tracker
[🚀 View the Live Executive Dashboard]
https://datastudio.google.com/s/oLKzu00XUQQ
# Real-Time Market Tracker & Data Pipeline

An automated data engineering project that tracks real-time stock market data, processes historical price trends, and feeds a live Executive Dashboard in Looker Studio.

## 🚀 Project Overview

This project automates the collection of financial data using Python and GitHub Actions. It implements a custom data schema that tracks not only the current price but also the `prev_price` to calculate real-time market momentum.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Libraries:** Pandas (Data Manipulation), Requests (API handling)
- **Automation:** GitHub Actions (Scheduled hourly triggers)
- **Storage:** CSV / GitHub Version Control
- **Visualization:** Looker Studio / Google Sheets

## 📊 Data Pipeline Architecture

1. **Extraction:** Python script fetches live market data via Alpha Vantage API.
2. **Transformation:** - Cleans timestamps and formats numerical data.
   - Implements a `prev_price` logic to compare current market value against the last recorded entry.
3. **Load:** Automatically commits the updated `market_history.csv` back to this repository.
4. **Visualization:** The CSV is synced to a Looker Studio dashboard via Google Sheets for real-time KPI tracking.

## 📈 Key Metrics Tracked

- **Latest Price:** Current market valuation.
- **Price Momentum:** Percentage change calculated as:
  $$((Price - Prev\_Price) / Prev\_Price) * 100$$
- **Volume Analysis:** Tracking trade frequency to identify market volatility.

## 📂 Repository Structure

- `tracker.py`: The core engine that fetches and processes data.
- `market_history.csv`: The historical database of all tracked tickers.
- `.github/workflows/`: Contains the automation logic for hourly updates.
