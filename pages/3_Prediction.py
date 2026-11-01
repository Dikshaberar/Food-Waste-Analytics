import streamlit as st
import pandas as pd

from sklearn.linear_model import LinearRegression

st.title("🤖 Economic Loss Prediction")

df = pd.read_csv(
    "archive (3)/global_food_wastage_dataset.csv"
)

X = df[["Total Waste (Tons)"]]

y = df["Economic Loss (Million $)"]

model = LinearRegression()

model.fit(X, y)

st.write(
    "Predict economic loss based on food waste."
)

waste = st.number_input(
    "Enter Food Waste in Tons",
    min_value=0,
    value=10000
)

if st.button("Predict Economic Loss"):

    prediction = model.predict(
        pd.DataFrame({
            "Total Waste (Tons)": [waste]
        })
    )[0]

    st.success(
        f"Predicted Economic Loss: ${prediction:,.2f} Million"
    )