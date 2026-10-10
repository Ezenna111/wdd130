import streamlit as st
import pandas as pd

st.set_page_config(page_title="Biz Monitor", page_icon="🏪")
st.title("🏪 Biz Monitor")
st.caption("Start empty. Add your products.")

# Empty private table for each person
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["product_name", "cost_price", "selling_price", "quantity"])

# THE TABLE - starts empty, you add rows
edited = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "product_name": st.column_config.TextColumn("Product Name"),
        "cost_price": st.column_config.NumberColumn("Cost Price ₦", min_value=0),
        "selling_price": st.column_config.NumberColumn("Selling Price ₦", min_value=0),
        "quantity": st.column_config.NumberColumn("Qty", min_value=0, step=1),
    },
    key="editor"
)

# Save for you only
if st.button("💾 Save", type="primary"):
    st.session_state.df = edited
    st.rerun()

# CALCULATION - only shows when you add something
if not edited.empty and len(edited.dropna(how='all')) > 0:
    df = edited.copy()
    df = df.dropna(subset=["product_name"])
    df["cost_price"] = pd.to_numeric(df["cost_price"], errors='coerce').fillna(0)
    df["selling_price"] = pd.to_numeric(df["selling_price"], errors='coerce').fillna(0)
    df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce').fillna(0)

    df["profit_each"] = df["selling_price"] - df["cost_price"]
    df["total_cost"] = df["cost_price"] * df["quantity"]
    df["total_sales"] = df["selling_price"] * df["quantity"]
    df["total_profit"] = df["profit_each"] * df["quantity"]

    st.divider()
    st.subheader("📊 Full Calculation")

    total_cost = df["total_cost"].sum()
    total_sales = df["total_sales"].sum()
    total_profit = df["total_profit"].sum()
    total_qty = df["quantity"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Items", f"{int(total_qty)}")
    c2.metric("Total Cost", f"₦{total_cost:,.0f}")
    c3.metric("Total Sales", f"₦{total_sales:,.0f}")
    c4.metric("Total Profit", f"₦{total_profit:,.0f}")

    st.dataframe(
        df[["product_name", "quantity", "cost_price", "selling_price", "profit_each", "total_cost", "total_sales", "total_profit"]],
        use_container_width=True
    )
else:
    st.info("👆 Table is empty. Click + to add your first product. Add product_name, cost_price, selling_price, quantity - you will see full total amount immediately.")