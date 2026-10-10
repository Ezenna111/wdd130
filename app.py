import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Biz Monitor", page_icon="🏪")
st.title("🏪 Biz Monitor")
st.write("My Small Business Tracker - Tap to Edit!")

CSV_FILE = "products.csv"

# Load or create file
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Create default
        data = {
            "product_name": ["Garri", "Rice", "Palm Oil", "Groundnut", "Fish"],
            "cost_price": [500, 1200, 2000, 300, 1500],
            "selling_price": [800, 1500, 2500, 500, 2000],
            "quantity": [20, 3, 10, 2, 8]
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)
        return df

df = load_data()

st.subheader("📝 Edit Your Products (Tap any cell)")

# Make it editable!
edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # You can add new rows!
    width='stretch',
    column_config={
        "product_name": st.column_config.TextColumn("Product Name", required=True),
        "cost_price": st.column_config.NumberColumn("Cost Price ₦", min_value=0, format="₦%d"),
        "selling_price": st.column_config.NumberColumn("Selling Price ₦", min_value=0, format="₦%d"),
        "quantity": st.column_config.NumberColumn("Quantity", min_value=0, step=1),
    }
)

# Save button
if st.button("💾 Save Changes", type="primary"):
    edited_df.to_csv(CSV_FILE, index=False)
    st.success("Saved! Your products updated.")
    st.rerun()

# Calculations
edited_df["profit_per_item"] = edited_df["selling_price"] - edited_df["cost_price"]
edited_df["total_profit"] = edited_df["profit_per_item"] * edited_df["quantity"]

st.divider()
st.subheader("📊 Report")

total_profit = edited_df["total_profit"].sum()
low_stock = edited_df[edited_df["quantity"] <= 5]

col1, col2 = st.columns(2)
col1.metric("Total Profit", f"₦{total_profit:,.0f}")
col2.metric("Low Stock Items", len(low_stock))

# Show profit table
display_df = edited_df.copy()
display_df["total_profit"] = display_df["total_profit"].apply(lambda x: f"₦{x:,.0f}")
st.dataframe(display_df, width='stretch')

if not low_stock.empty:
    st.warning(f"⚠️ Buy more: {', '.join(low_stock['product_name'].tolist())}")
else:
    st.success("All stock OK ✅")

st.caption(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")