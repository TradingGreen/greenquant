import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# Set page config (mobile friendly, Robinhood-style green theme)
st.set_page_config(page_title="GreenQuant", layout="wide", initial_sidebar_state="collapsed")

# Custom styling for dark green look
st.markdown("""
    <style>
    body {
        background-color: #0f1d1d;
        color: #d8f3dc;
    }
    .main {
        background-color: #0f1d1d;
    }
    .stButton>button {
        color: #fff;
        background-color: #1b4332;
        border-color: #95d5b2;
        font-weight: bold;
        padding: 0.5em 1.2em;
        border-radius: 8px;
    }
    .stDataFrame, .stTable {
        background-color: #0f1d1d;
        color: #d8f3dc;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Trade ideas (demo data — will later come from GPT or DB)
trades = [
    {"Date": "2025-06-25", "Ticker": "AAPL", "Asset Name": "Apple Inc.", "Asset Type": "Stock", "Quantity": 10, "Buy Price": 210},
    {"Date": "2025-06-28", "Ticker": "BTC-USD", "Asset Name": "Bitcoin", "Asset Type": "Crypto", "Quantity": 0.05, "Buy Price": 62000},
    {"Date": "2025-06-30", "Ticker": "NVDA", "Asset Name": "Nvidia", "Asset Type": "Stock", "Quantity": 5, "Buy Price": 125},
    {"Date": "2025-06-26", "Ticker": "ETH-USD", "Asset Name": "Ethereum", "Asset Type": "Crypto", "Quantity": 0.2, "Buy Price": 3400},
]

# Create DataFrame
df = pd.DataFrame(trades)

# 🔁 Get current price from Yahoo Finance
def get_current_price(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1d", progress=False)
        return data["Close"].iloc[-1] if not data.empty else None
    except:
        return None

df["Current Price"] = df["Ticker"].apply(get_current_price)

# 💸 Core calculations
df["Entry Cost"] = df["Buy Price"] * df["Quantity"]
df["Current Value"] = df["Current Price"] * df["Quantity"]
df["Unrealized P/L"] = df["Current Value"] - df["Entry Cost"]
df["% Return"] = ((df["Current Value"] - df["Entry Cost"]) / df["Entry Cost"]) * 100

# 📈 Summary values
total_entry = df["Entry Cost"].sum()
total_current = df["Current Value"].sum()
total_return = total_current - total_entry
total_return_pct = (total_return / total_entry) * 100

# ✅ APP HEADER
st.title("💹 GreenQuant: Mobile Quant Portfolio")
st.markdown("A smart, AI-enhanced trading assistant for young investors.")

# 🔥 Trade Signals
st.subheader("🧠 Today's AI-Powered Trade Ideas")

for idx, row in df.iterrows():
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"### {row['Asset Name']} ({row['Ticker']})")
        st.markdown(f"**Type:** {row['Asset Type']}  |  **Quantity:** {row['Quantity']}")
        st.markdown(f"📈 **Entry Price:** ${row['Buy Price']:.2f}  →  **Now:** ${row['Current Price']:.2f}")
        st.markdown(f"💸 **Return:** `{row['% Return']:.2f}%`")
        st.markdown(f"🧠 *Why this trade?* \n> _\"AI identified strong sector momentum, price breakout, and volume spike.\"_")
    with col2:
        st.button("✅ I followed this trade", key=f"trade_{idx}")

# 📊 Portfolio Summary
st.markdown("---")
st.subheader("📊 Paper Portfolio Performance")

summary = pd.DataFrame({
    "Metric": ["Total Invested", "Current Value", "Unrealized P/L", "Total Return %"],
    "Value": [f"${total_entry:,.2f}", f"${total_current:,.2f}", f"${total_return:,.2f}", f"{total_return_pct:.2f}%"]
})

st.table(summary)

# Footer
st.caption("🟢 Powered by AI. Data from Yahoo Finance.")
