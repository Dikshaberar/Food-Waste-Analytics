import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load data
df = pd.read_csv("FoodWasteAnalytics/archive (3)/global_food_wastage_dataset.csv")

# 2. Input (X) and output (y)
X = df[["Total Waste (Tons)"]]
y = df["Economic Loss (Million $)"]

# 3. Split: 80% to teach, 20% to test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Test it on unseen data
pred = model.predict(X_test)
print("R2 score:", round(r2_score(y_test, pred), 3))
print("Average error (Million $):", round(mean_absolute_error(y_test, pred), 2))
print("Loss per ton ($M):", round(model.coef_[0], 4))

# 6. Predict for a new value
new = pd.DataFrame({"Total Waste (Tons)": [10000]})
print("Predicted loss for 10,000 tons:", round(model.predict(new)[0], 2), "Million $")

# 7. Chart
line = pd.DataFrame({"Total Waste (Tons)": [X.iloc[:, 0].min(), X.iloc[:, 0].max()]})
plt.scatter(X_test, y_test, s=8, label="Actual")
plt.plot(line, model.predict(line), color="red", label="Model line")
plt.xlabel("Total Waste (Tons)")
plt.ylabel("Economic Loss (Million $)")
plt.title("Predicting Economic Loss from Food Waste")
plt.legend()
plt.savefig("model_chart.png")
plt.show()