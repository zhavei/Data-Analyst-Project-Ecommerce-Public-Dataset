import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from BaseFunc import BaseFunc

import os

sns.set(style='dark')

# Dataset
datetime_cols = ["shipping_limit_date", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df = pd.read_csv("combined_dataset.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)


for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("logo.png"
                 , width=100)
    with col3:
        st.write(' ')

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]


helper_func = BaseFunc(main_df)

daily_orders_df = helper_func.create_daily_orders_df()
sum_order_items_df = helper_func.create_sum_order_items_df()
order_status, common_status = helper_func.create_order_status() # still not used

# Define your Streamlit app
st.title("E-Commerce Public Data Analysis")

# Add text or descriptions
st.write("**This is a dashboard for analyzing E-Commerce public data.**")



# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = daily_orders_df["revenue"].sum()
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders_df["order_approved_at"],
    y=daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)