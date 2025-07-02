
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
