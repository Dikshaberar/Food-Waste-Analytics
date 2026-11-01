import pandas as pd

df = pd.read_csv("FoodWasteAnalytics/archive (3)/global_food_wastage_dataset.csv")

print("Countries:", sorted(df["Country"].unique()))
print("Categories:", sorted(df["Food Category"].unique()))

country  = input("\nEnter country: ").strip()
category = input("Enter food category: ").strip()
cut      = float(input("Reduce waste by (%): "))

# Filter rows for this country + category
sub = df[(df["Country"].str.lower() == country.lower()) &
         (df["Food Category"].str.lower() == category.lower())]

if sub.empty:
    print("No data found. Check the spelling.")
else:
    tons = sub["Total Waste (Tons)"].sum()
    loss = sub["Economic Loss (Million $)"].sum()

    saved_tons = tons * cut / 100
    saved_loss = loss * cut / 100

    print("\n===== WHAT-IF RESULT =====")
    print(f"Current waste     : {tons:,.0f} tons")
    print(f"Current loss      : {loss:,.0f} million $")
    print(f"After {cut}% cut   : {tons - saved_tons:,.0f} tons")
    print(f"Waste saved       : {saved_tons:,.0f} tons")
    print(f"Money saved       : {saved_loss:,.0f} million $")