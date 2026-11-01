# ===== FOOD WASTE ANALYTICS =====
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# ---- 1. CONFIG ----
FILE     = "FoodWasteAnalytics/archive (3)/global_food_wastage_dataset.csv"
COUNTRY  = "Country"
YEAR     = "Year"
CATEGORY = "Food Category"
WASTE    = "Total Waste (Tons)"
LOSS     = "Economic Loss (Million $)"
PERCAP   = "Avg Waste per Capita (Kg)"
HOUSE    = "Household Waste (%)"

# ---- 2. LOAD & INSPECT ----
df = pd.read_csv(FILE)
print("Shape:", df.shape)
print(df.head())
df.info()
print("Missing values:\n", df.isnull().sum())

# ---- 3. CLEAN ----
df = df.drop_duplicates()
df = df.dropna()
print("After cleaning:", df.shape)

# ---- 4. ANALYSIS + CHARTS ----

# (a) Top 10 countries by total waste
top_countries = df.groupby(COUNTRY)[WASTE].sum().sort_values(ascending=False).head(10)
print("\nTop 10 countries:\n", top_countries)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_countries.values, y=top_countries.index, color="tomato")
plt.title("Top 10 Countries by Total Food Waste")
plt.xlabel("Total Waste (Tons)")
plt.tight_layout()
plt.savefig("top_countries.png")
plt.show()

# (b) Waste by food category
cat_waste = df.groupby(CATEGORY)[WASTE].sum().sort_values(ascending=False)
print("\nWaste by category:\n", cat_waste)
plt.figure(figsize=(10, 5))
sns.barplot(x=cat_waste.index, y=cat_waste.values, color="seagreen")
plt.title("Food Waste by Category")
plt.xticks(rotation=45)
plt.ylabel("Total Waste (Tons)")
plt.tight_layout()
plt.savefig("category_waste.png")
plt.show()

# (c) Yearly trend
yearly = df.groupby(YEAR)[WASTE].sum()
print("\nYearly waste:\n", yearly)
plt.figure(figsize=(8, 4))
plt.plot(yearly.index, yearly.values, marker="o", color="green")
plt.title("Food Waste Trend Over the Years")
plt.xlabel("Year")
plt.ylabel("Total Waste (Tons)")
plt.tight_layout()
plt.savefig("yearly_trend.png")
plt.show()

# (d) Economic loss by category
cat_loss = df.groupby(CATEGORY)[LOSS].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x=cat_loss.index, y=cat_loss.values, color="darkorange")
plt.title("Economic Loss by Food Category")
plt.xticks(rotation=45)
plt.ylabel("Loss (Million $)")
plt.tight_layout()
plt.savefig("economic_loss.png")
plt.show()

# (e) Top 10 countries by waste per capita
percap = df.groupby(COUNTRY)[PERCAP].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=percap.values, y=percap.index, color="steelblue")
plt.title("Top 10 Countries by Avg Waste per Capita")
plt.xlabel("Kg per person")
plt.tight_layout()
plt.savefig("per_capita.png")
plt.show()

# (f) Household waste % by country (top 10)
house = df.groupby(COUNTRY)[HOUSE].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=house.values, y=house.index, color="mediumpurple")
plt.title("Top 10 Countries by Household Waste %")
plt.xlabel("Household Waste (%)")
plt.tight_layout()
plt.savefig("household_waste.png")
plt.show()

# (g) Correlation heatmap
plt.figure(figsize=(9, 6))
sns.heatmap(df.select_dtypes("number").corr(), annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Correlation Between Numeric Columns")
plt.tight_layout()
plt.savefig("correlation.png")
plt.show()

# ---- 5. INSIGHTS ----
print("\n===== KEY INSIGHTS =====")
print("Highest waste country   :", top_countries.index[0])
print("Most wasted food type   :", cat_waste.index[0])
print("Highest economic loss   :", cat_loss.index[0])
print("Year with most waste    :", yearly.idxmax())
print("Highest per capita      :", percap.index[0])
print("Total waste (all data)  : {:,.0f} tons".format(df[WASTE].sum()))