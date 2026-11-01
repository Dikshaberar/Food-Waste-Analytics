import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Food Waste Dashboard")

df = pd.read_csv(
    "archive (3)/global_food_wastage_dataset.csv"
)

# Statistics

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Food Waste",
    f"{df['Total Waste (Tons)'].sum():,.0f} Tons"
)

col2.metric(
    "Economic Loss",
    f"${df['Economic Loss (Million $)'].sum():,.2f}M"
)

col3.metric(
    "Total Countries",
    df["Country"].nunique()
)

st.markdown("---")

# Country analysis

country_data = (
    df.groupby("Country")["Total Waste (Tons)"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig = px.bar(
    country_data,
    x="Country",
    y="Total Waste (Tons)",
    color="Total Waste (Tons)",
    color_continuous_scale="Greens",
    title="Top 10 Countries by Food Waste"
)

st.plotly_chart(fig, use_container_width=True)

# Category analysis

category_data = (
    df.groupby("Food Category")["Total Waste (Tons)"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    category_data,
    names="Food Category",
    values="Total Waste (Tons)",
    hole=0.5,
    title="Food Waste by Category"
)

st.plotly_chart(fig2, use_container_width=True)