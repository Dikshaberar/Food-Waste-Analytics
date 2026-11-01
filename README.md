# Food Waste Analytics

A Python data analysis project on global food waste (2018-2024). It cleans the data, finds patterns, predicts economic loss, and shows everything in a Streamlit dashboard.

## What it does
- Shows total waste, economic loss, waste per person and household share
- Finds the top countries and the most wasted food categories
- Shows the yearly waste trend
- Predicts economic loss from waste using Linear Regression (R² = 0.951)
- Has a simulator that shows food and money saved when waste is reduced

## Key results
- Total food waste: 125,308,900 tons
- Highest waste country: Turkey
- Most wasted category: Prepared Food
- Peak year: 2023

## Dataset
Global Food Wastage Dataset (2018-2024) from Kaggle: 5,000 records, 20 countries, 8 food categories, 7 years.

## Technologies
Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Plotly, Streamlit

## Project files
- `app.py`: home page of the Streamlit app
- `pages/`: Dashboard, Prediction, Simulator and About pages
- `food_waste.py`: data cleaning, analysis and charts
- `model.py`: prediction model
- `simulator.py`: waste reduction simulator
- `requirements.txt`: required libraries

## How to run
1. Install the libraries:
   `pip install -r requirements.txt`
2. Start the app:
   `streamlit run app.py`

## Author
Diksha
