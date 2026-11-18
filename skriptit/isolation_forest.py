import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');
df_test = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_testing-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label", "proto", "service", "state"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

y_test = df_test['label']
df_test = df_test.drop(["id", "attack_cat", "label", "proto", "service", "state"], axis=1)
print(df_test.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df_test = pd.get_dummies(df_test)
columns_test = df_test.columns

contamination = 0.50
model = IsolationForest(contamination=contamination).fit(df)
pred = model.predict(df) == -1
poikkeavuusarvot = -model.score_samples(df)

df1 = pd.DataFrame({
    "poikkeavuusarvot": poikkeavuusarvot,
    "label": y.values}, index=df.index+1)

print("Maksimit:\n\n", df1.sort_values(ascending=False, by='poikkeavuusarvot').head(5))

print(poikkeavuusarvot)

# Arvioidaan menetelmää usealla eri kynnyksellä 
thresholds = np.percentile(poikkeavuusarvot, [40, 70, 80, 85, 90, 95, 99])
y_true = (y == 1).astype(int)  

print("kynnys   hälytykset     TP         FP         FN     precision  recall  F1")
for tau in thresholds:
    pred = (poikkeavuusarvot >= tau).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()
    p = precision_score(y_true, pred, zero_division=0)
    r = recall_score(y_true, pred, zero_division=0)
    f1 = f1_score(y_true, pred, zero_division=0)
    print(f"{tau:5.2f} {pred.sum():10d} {tp:10d} {fp:10d} {fn:10d} {p:10.2f} {r:7.2f} {f1:5.2f}")
