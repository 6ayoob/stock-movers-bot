import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def load_symbols():
    with open("symbols.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

def scan_stocks(max_price=20, limit=10):
    symbols = load_symbols()
    passed = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="6mo")

            if len(df) < 50:
                continue

            current_price = df["Close"].iloc[-1]
            volume_today = df["Volume"].iloc[-1]
            volume_avg_50 = df["Volume"].rolling(50).mean().iloc[-1]
            ma50 = df["Close"].rolling(50).mean().iloc[-1]

            if (
                current_price < max_price
                and current_price > ma50
                and volume_today > volume_avg_50
            ):
                passed.append((symbol, current_price, volume_today))
        except Exception:
            continue

    # ترتيب حسب السعر التنازلي (أو الحجم)
    passed = sorted(passed, key=lambda x: x[1], reverse=True)
    return passed[:limit]
