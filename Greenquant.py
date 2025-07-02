# User-defined trade signals
trades = [
    {"Date": "2025-06-25", "Ticker": "AAPL", "Asset Name": "Apple Inc.", "Asset Type": "Stock", "Quantity": 10, "Buy Price": 210},
    {"Date": "2025-06-28", "Ticker": "BTC-USD", "Asset Name": "Bitcoin", "Asset Type": "Crypto", "Quantity": 0.05, "Buy Price": 62000},
    {"Date": "2025-06-30", "Ticker": "NVDA", "Asset Name": "Nvidia", "Asset Type": "Stock", "Quantity": 5, "Buy Price": 125},
    {"Date": "2025-06-26", "Ticker": "ETH-USD", "Asset Name": "Ethereum", "Asset Type": "Crypto", "Quantity": 0.2, "Buy Price": 3400},
]

# Convert to DataFrame
df = pd.DataFrame(trades)

# Get real-time current prices
def get_current_price(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1d", progress=False)
        return data["Close"].iloc[-1] if not data.empty else None
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None

df["Current Price"] = df["Ticker"].apply(get_current_price)

# Calculate core portfolio metrics
df["Entry Cost"] = df["Buy Price"] * df["Quantity"]
df["Current Value"] = df["Current Price"] * df["Quantity"]
df["Unrealized P/L"] = df["Current Value"] - df["Entry Cost"]
df["% Return"] = ((df["Current Value"] - df["Entry Cost"]) / df["Entry Cost"]) * 100

# Portfolio Summary
total_entry = df["Entry Cost"].sum()
total_current = df["Current Value"].sum()
total_return = total_current - total_entry
total_return_pct = (total_return / total_entry) * 100

summary = pd.DataFrame({
    "Metric": ["Total Invested", "Current Value", "Unrealized P/L", "Total Return %"],
    "Value": [f"${total_entry:,.2f}", f"${total_current:,.2f}", f"${total_return:,.2f}", f"{total_return_pct:.2f}%"]
})

# Output to console
print("\n📈 Trade Signal Performance")
print(df[["Date", "Ticker", "Quantity", "Buy Price", "Current Price", "Unrealized P/L", "% Return"]])

print("\n📊 Portfolio Summary")
print(summary)
