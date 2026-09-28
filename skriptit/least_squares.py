import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

X = df[["dur"]]
y = df["sbytes"]

model = LinearRegression().fit(X, y)
pred = model.predict(X)
residual = y - pred
print(residual)

print("Minimit:\n\n", residual.sort_values().head(5))
print("")
print("--------------------------------------")
print("")
print("Maksimit:\n\n", residual.sort_values(ascending=False).head(5))

df = pd.DataFrame(residual, None)
df.to_csv('least_squares.csv')