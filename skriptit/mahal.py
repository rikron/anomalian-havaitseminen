import pandas as pd
import numpy as np
import scipy

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

numeeriset = df.select_dtypes(include=np.number)

def mahalanobis(df):
    cov = df.cov().values
    inv_cov = np.linalg.inv(cov)
    mean = df.mean().values
    scores = []
    values = df.values
    for i in range(values.shape[0]):
        score = scipy.spatial.distance.mahalanobis(mean, values[i], inv_cov)
        scores.append(score)
    return pd.DataFrame({
    "poikkeavuusarvot": scores,
    "label": y.values})



valitut = numeeriset[["dur", "rate", "sbytes", "dbytes"]]

mahal = mahalanobis(valitut)
print("Mahalanobis:\n\n", mahal)
mahal.to_csv('mahalanobis.csv')

print("Minimit:\n\n", mahal.sort_values(by="poikkeavuusarvot").head(5))
print("")
print("--------------------------------------")
print("")
print("Maksimit:\n\n", mahal.sort_values(by="poikkeavuusarvot", ascending=False).head(5))

threshold_95 = np.percentile(mahal, 95)
threshold_99 = np.percentile(mahal, 99)

print(f"95. persentiilin kynnysarvo: {threshold_95:.6f}")
print(f"99. persentiilin kynnysarvo: {threshold_99:.6f}")
