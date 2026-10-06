import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn import random_projection

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

D0 = pairwise_distances(df)

transformer = random_projection.GaussianRandomProjection(n_components=15)
X_new = transformer.fit_transform(df)
print(X_new.shape)