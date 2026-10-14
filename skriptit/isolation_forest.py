import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

contamination = 0.30
model = IsolationForest(contamination=contamination).fit(df)
pred = model.predict(df) == -1
poikkeavuusarvot = -model.score_samples(df)

df1 = pd.DataFrame({
    "poikkeavuusarvot": poikkeavuusarvot,
    "label": y.values})

print("Maksimit:\n\n", df1.sort_values(ascending=False, by='poikkeavuusarvot').head(5))

print(poikkeavuusarvot)

threshold_95 = np.percentile(poikkeavuusarvot, 95)
threshold_99 = np.percentile(poikkeavuusarvot, 99)

print(f"95. persentiilin kynnysarvo: {threshold_95:.6f}")
print(f"99. persentiilin kynnysarvo: {threshold_99:.6f}")
