import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = {
    "Monthly_Hours": [100,150,200,250,300,350,400,450,500],
    "Tariff": [6,6.5,7,7.5,8,8.5,9,9.5,10],
    "Bill": [600,975,1400,1875,2400,2975,3600,4275,5000]
}

df = pd.DataFrame(data)

X = df[["Monthly_Hours", "Tariff"]]
y = df["Bill"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "bill_model.pkl")

print("Model saved: bill_model.pkl")
