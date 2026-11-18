import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

df_train = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv')
df_test = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df_train['label']
df_train = df_train.drop(["id", "attack_cat", "label", "proto", "service", "state"], axis=1)
print(df_train.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df_train = pd.get_dummies(df_train)
columns = df_train.columns

y = df_test['label']
df_test = df_test.drop(["id", "attack_cat", "label", "proto", "service", "state"], axis=1)
print(df_test.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df_test = pd.get_dummies(df_test)
columns = df_test.columns

X_train = df_train.astype(float)

scaler_test = RobustScaler().fit(X_train)
X_test = scaler_test.transform(X_train)

X = df_test.astype(float)

scaler = RobustScaler().fit(X)
Xs = scaler.transform(X)

hidden = 16,
ae = MLPRegressor(hidden_layer_sizes=hidden, activation="tanh", max_iter=4000).fit(X_test[:10000], X_test[:10000])
recon = ae.predict(Xs)
err = np.linalg.norm(Xs - recon, axis=1)
print("hidden", hidden, "top5", np.argsort(err)[-5:][::-1].tolist(), "outlier-virheet", np.round(err[-2:], 2), "...", np.round(err[:2], 2))

# Tehdään uusi dataframe, jonne yhdistetään labelit ja häviöt
new_df = pd.DataFrame({
    "rekonstruktiohäviö": np.round(err, 4),
    "label": y.values}, index=df_test.index+1)

new_df.sort_values(by="rekonstruktiohäviö", ascending=False)

new_df.to_csv("csv/autoenkooderi.csv")

print(new_df.sort_values("rekonstruktiohäviö", ascending=False).head(10))

# Arvioidaan menetelmää usealla eri kynnyksellä 
thresholds = np.percentile(err, [40, 70, 80, 85, 90, 95, 99])
y_true = (y == 1).astype(int)  

print("kynnys   hälytykset     TP         FP         FN     precision  recall  F1")
for tau in thresholds:
    pred = (err >= tau).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()
    p = precision_score(y_true, pred, zero_division=0)
    r = recall_score(y_true, pred, zero_division=0)
    f1 = f1_score(y_true, pred, zero_division=0)
    print(f"{tau:5.2f} {pred.sum():10d} {tp:10d} {fp:10d} {fn:10d} {p:10.2f} {r:7.2f} {f1:5.2f}")