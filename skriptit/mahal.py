import pandas as pd
import numpy as np
import scipy
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

numeeriset = df.select_dtypes(include=np.number)
poikkeavuusarvot = []
def mahalanobis(df):
    cov = df.cov().values
    inv_cov = np.linalg.inv(cov)
    mean = df.mean().values
    values = df.values
    for i in range(values.shape[0]):
        score = scipy.spatial.distance.mahalanobis(mean, values[i], inv_cov)
        poikkeavuusarvot.append(score)
    return pd.DataFrame({
    "poikkeavuusarvot": poikkeavuusarvot,
    "label": y.values})

valitut = numeeriset[["dur", "rate", "sbytes", "dbytes"]]

mahal = mahalanobis(valitut)
print("Mahalanobis:\n\n", mahal)
mahal.to_csv('csv/mahalanobis.csv')

print("Minimit:\n\n", mahal.sort_values(by="poikkeavuusarvot").head(5))
print("")
print("--------------------------------------")
print("")
print("Maksimit:\n\n", mahal.sort_values(by="poikkeavuusarvot", ascending=False).head(5))

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
