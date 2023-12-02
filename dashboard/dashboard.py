import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from BaseFunc import BaseFunc
sns.set(style='white')

import os

# Dataset
datetime_cols = ["shipping_limit_date", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df = pd.read_csv("https://raw.githubusercontent.com/zhavei/Data-Analyst-Project-Ecommerce-Public-Dataset/master/dashboard/combined_dataset.csv")
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
        st.image("https://raw.githubusercontent.com/zhavei/Data-Analyst-Project-Ecommerce-Public-Dataset/master/dashboard/logo.jpg"
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
# best favorite product function
sum_order_items_df = helper_func.create_sum_order_items_df()

# Define your Streamlit app
st.title("Brassil E-Commerce Public Data Analysis")

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

###################################################################################
#Top 5 Favorites Product by Categories
st.subheader("Top 5 Favorites Product  by Categories")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))


sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette="viridis", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=80)
ax[0].set_title("Most sold products", loc="center", fontsize=90)
ax[0].tick_params(axis ='y', labelsize=55)
ax[0].tick_params(axis ='x', labelsize=50)

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette="viridis", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Fewest products sold", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)
###################################################################################

# Top 5 categories by revenue
# Groupby and sum prices
def create_order_revenue(df):
    order_revenue_df = df[df['order_status'] == 'delivered']\
        .groupby('product_category_name_english')['price'].agg(['sum', 'count']).reset_index()

    # Sort by total price and keep top 5
    order_revenue_df = order_revenue_df.sort_values('sum', ascending=False).head(5).reset_index()

    return order_revenue_df

# revenue function
order_revenue_df = create_order_revenue(main_df)

# Categories By Revenue
st.subheader("Best Product Categories By Revenue")

# Membagi layout menjadi dua kolom
col1, col2 = st.columns(2)

# Menampilkan informasi pada kolom pertama
with col1:
    total_items = order_revenue_df["count"].sum()
    st.markdown(f"Total Items: **{total_items}**")
    
with col2:
    total_price = order_revenue_df["sum"].sum()
    st.markdown(f"Total Price: **${total_price:,.2f}**")
    

# Plot bar chart
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="product_category_name_english",
    y="sum",
    data=order_revenue_df.sort_values(by="sum", ascending=False),
    palette='viridis',
    ax=ax
    )
ax.set_title("Number of Categories by Revenues", loc="center", fontsize=30)
ax.set_ylabel("Total Price", fontsize=20)
ax.set_xlabel("Product Category", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

    # Menambahkan label pada sumbu x
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Menambahkan label harga pada setiap batang
for p in ax.patches:
    ax.annotate(f"${p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=15, color='black', xytext=(0, 5),
                textcoords='offset points')

# Menampilkan visualisasi pada Streamlit
st.pyplot(fig)
    
###################################################################################

#dimanakah pesanan/kostomer terbanyak berdasarkan kota?
def customer_city(df):
    order_by_city = df[df['order_status'] == 'delivered'].groupby('customer_city')\
                        .agg({'order_id':'count'})\
                        .sort_values('order_id',ascending=False)\
                        .reset_index()
    return order_by_city  # top 5 customer by city

def customer_state(df):
    order_by_state = df[df['order_status'] == 'delivered'].groupby('customer_state')\
                        .agg({'order_id':'count'})\
                        .sort_values('order_id',ascending=False)\
                        .reset_index()
    return order_by_state  # top 5 customer by state

order_by_city = customer_city(main_df)
order_by_state = customer_state(main_df)

# Visualisasi dengan Seaborn dan Streamlit----------------
st.subheader('Top 5 Customer By City & State')
col1, col2 = st.columns(2)

with col1:
    total_customer_city = order_by_city["order_id"].count()
    st.markdown(f"Total Customer by City: **{total_customer_city}**")

with col2:
    total_customer_state = order_by_state["order_id"].mean()
    st.markdown(f"Average Customer by State: **{total_customer_state}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_id", y="customer_city", data=order_by_city.head(5), palette='viridis', ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer City", fontsize=30)
ax[0].set_title("Top 5 Kostumer Berdasarkan Kota", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="order_id", y="customer_state", data=order_by_state.head(5), palette='viridis', ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer State", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Top 5 Kostumer Berdasarkan State", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

###################################################################################

# seller berdasarkan seller city dan mengagregasi berdasarkan total harga & orderan
def seller_city(df):
    sales_by_city = df[df['order_status'] == 'delivered'].groupby('seller_city')\
                        .agg({'price':'sum', 'order_id': 'count'})\
                        .rename(columns={'price':'total_sales', 'order_id':'total_order'})\
                        .reset_index()
    return sales_by_city.nlargest(5, 'total_sales')  # Filter top 5 sellers

# seller berdasarkan seller state dan mengagregasi berdasarkan total harga & orderan
def seller_state(df):
    sales_by_state = df[df['order_status'] == 'delivered'].groupby('seller_state')\
                        .agg({'price':'sum', 'order_id': 'count'})\
                        .rename(columns={'price':'total_sales', 'order_id':'total_order'})\
                        .reset_index()
    return sales_by_state.nlargest(5, 'total_sales')  # Filter top 5 sellers

# revenue function
sales_by_city = seller_city(main_df)
sales_by_state = seller_state(main_df)

# Seller By City & State (Top 5)
st.subheader("Top 5 Best Sellers Performer By City & State")
#--------------------------------------------------
# Create tabs
tabs = st.tabs(["By City", "By State"])

# Tab 1: By City
with tabs[0]:
    total_sellers_city = sales_by_city["total_sales"].sum()
    st.markdown(f"Total Revenue: **${total_sellers_city:,.2f}**")

    # Plot bar chart for sellers by city (Top 5)
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="seller_city",
        y="total_sales",
        data=sales_by_city.sort_values(by="total_sales", ascending=False),
        palette='viridis',
        ax=ax
    )
    ax.set_title("Top 5 Performer Sellers by City", loc="center", fontsize=30)
    ax.set_ylabel("Total Sales", fontsize=20)
    ax.set_xlabel("Seller City", fontsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Add price labels on each bar
    for p in ax.patches:
        ax.annotate(f"${p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=15, color='black', xytext=(0, 5),
                    textcoords='offset points')

    # Show the plot
    st.pyplot(fig)

# Tab 2: By State
with tabs[1]:
    total_sellers_state = sales_by_state["total_sales"].sum()
    st.markdown(f"Total Revenue: **${total_sellers_state:,.2f}**")

    # Plot bar chart for sellers by state (Top 5)
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="seller_state",
        y="total_sales",
        data=sales_by_state.sort_values(by="total_sales", ascending=False),
        palette='viridis',
        ax=ax
    )
    ax.set_title("Top 5 Performer Sellers by State", loc="center", fontsize=30)
    ax.set_ylabel("Total Sales", fontsize=20)
    ax.set_xlabel("Seller State", fontsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Add price labels on each bar
    for p in ax.patches:
        ax.annotate(f"${p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=15, color='black', xytext=(0, 5),
                    textcoords='offset points')

    # Show the plot
    st.pyplot(fig)

#################################################################

st.caption("Copyright © Syafe'ie 2023")