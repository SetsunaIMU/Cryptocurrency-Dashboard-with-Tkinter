# Crypto Trading Dashboard

A Python program about **Crypto Trading Dashboard** by using **Tkinter** and **Binance REST API** to display real-time cryptocurrency market data, technical analysis, and recent trades.

This project demonstrates both dashboard features, including Ticker, Order Book, Chart, Indicators, and Recent Trade 

---

## Features Overview

### Real-time Market Data
* Order Book visualization (Bids/Asks)
* Auto-refresh every 2 seconds
* Candlestick chart using Binance data

### UI
* Multi crypto currency support (BTC, ETH, SOL, BNB, DOGE, LUNA)
* Dropdown menu
* Dashboard panels (toggle on/off)
* Green color for profit 
* red color for loss otherwise in market trade, if it becomes red, that means the user sells crypto and green color means the user buys crypto

### Technical Analysis
* Candlestick chart time intervals: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
* Technical indicators:

  * RSI (Relative Strength Index)
  * Moving Average (MA)
  * Bollinger Bands (Upper / Middle / Lower)

---

## Project Structure

```
project/
│
├── main.py                     # Application entry point
├── config.py                   # Symbols, colors, chart intervals
├── requirements.txt            # Necessary Library for this project
│
├── components/                 # UI components
│   ├── ticker.py               # Real time price ticker
│   ├── orderbook.py            # Order book panel
│   ├── technical.py            # Technical analysis chart
│   ├── market_trade.py         # Recent trades panel
│   └── __init__.py
│
├── utils/                      # Data & indicator utilities
│   ├── binance_api.py          # Binance REST & WebSocket 
│   ├── indicators.py           # RSI, MA, Bollinger Bands, MACD
│   └── __init__.py
│
└── preferences.json            # User preferences
```

---

## Requirements

* **Python 3.9+**
* **Tkinter / ttk** – GUI framework
* **Matplotlib** – Chart rendering
* **NumPy** – Indicator calculations
* **requests** -REST API
* **Threading** – Background data fetching
* **websocket** -Real-time WebSocket connections

---

## How to Run

1. Clone the repository

``` bash
https://github.com/SetsunaIMU/Cryptocurrency-Dashboard-with-Tkinter
cd Cryptocurrency-Dashboard-with-Tkinter
```

2. Install the requirements for the project.

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

---

## Notes
* Need internet to connect for live data
* Preferences are saved automatically on exit

## IF you can't watch the video you can click this link
https://drive.google.com/file/d/1PKzU5BydfbLrUN2rS7FSk8GYM2gr41Mn/view?usp=sharing

