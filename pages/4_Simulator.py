import streamlit as st
import pandas as pd

st.title("🌍 Food Waste Reduction Simulator")

df = pd.read_csv(
    "archive (3)/global_food_wastage_dataset.csv"
)

country = st.selectbox(
    "Select Country",
    sorted(df["Country"].unique())
)

category = st.selectbox(
    "Select Food Category",
    sorted(df["Food Category"].unique())
)

reduction = st.slider(
    "Waste Reduction Percentage",
    0, 90, 20
)

data = df[
    (df["Country"] == country) &
    (df["Food Category"] == category)
]

if not data.empty:

    waste = data["Total Waste (Tons)"].sum()

    loss = data["Economic Loss (Million $)"].sum()

    saved_waste = waste * reduction / 100

    saved_money = loss * reduction / 100

    st.metric(
        "Waste Saved",
        f"{saved_waste:,.2f} Tons"
    )

    st.metric(
        "Money Saved",
        f"${saved_money:,.2f} Million"
    )

    st.metric(
        "Remaining Waste",
        f"{waste-saved_waste:,.2f} Tons"
    )