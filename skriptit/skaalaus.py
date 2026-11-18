import pandas as pd
from sklearn.preprocessing import RobustScaler

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

""" Pudotetaan valmiit label arvot ja id """
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df)

"""One-hot-koodataan kategoriset arvot"""
df = pd.get_dummies(df)

columns = df.columns
"""Skaalataan robustilla menetelmällä"""
scaler = RobustScaler()
df = scaler.fit_transform(df)
df = pd.DataFrame(df, None, columns=columns)

"""CSV tiedostoksi muunnettu taulukko"""
print(df)
df.to_csv('csv/skaalattu.csv', index=False)