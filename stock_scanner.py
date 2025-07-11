import yfinance as yf
import pandas as pd

# تحميل قائمة مخصصة من الأسهم (يفضل تحميلها من ملف خارجي لو كانت كبيرة)
def load_stock_list():
    # يمكنك استبدال هذه القائمة بـ 3000 سهم لاحقًا
    return [
        "AAPL", "AMD", "INTC", "F", "T", "GE", "SNAP", "XRX", "ZNGA", "UAL",
        "PFE", "NOK", "FCEL", "SIRI", "WISH", "GPRO", "BB", "KODK", "SOFI", "PLTR"
    ]

def scan_stocks(symbols):
    qualified_stocks = []

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            price = info.get("regularMarketPrice", 0)
            avg_volume = info.get("averageVolume", 0)
            volume = info.get("volume", 0)
            fifty_day_avg = info.get("fiftyDayAverage", 0)

            if price and price < 20 and volume > avg_volume and price > fifty_day_avg:
                qualified_stocks.append({
                    "Symbol": symbol,
                    "Name": info.get("shortName", symbol),
                    "Price": price,
                    "Volume": volume,
                    "50-Day Avg": fifty_day_avg
                })
        except Exception:
            continue

    return pd.DataFrame(qualified_stocks)

if __name__ == "__main__":
    stock_list = load_stock_list()
    results = scan_stocks(stock_list)

    if not results.empty:
        print("✅ أفضل الأسهم حسب الشروط المحددة:")
        print(results.head(10).to_string(index=False))
    else:
        print("❌ لا توجد أسهم تحقق الشروط حالياً.")
