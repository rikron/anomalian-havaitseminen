import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import RobustScaler

df_train = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv')

# Pudotetaan valmiit label arvot ja id, label talteen
y = df_train['label']
df_train = df_train.drop(["id", "attack_cat", "label"], axis=1)
print(df_train.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df_train = pd.get_dummies(df_train)
columns = df_train.columns

X = df_train.astype(float)

scaler = RobustScaler().fit(X)
Xs = scaler.transform(X)

hidden = 16,
ae = MLPRegressor(hidden_layer_sizes=hidden, activation="tanh", max_iter=4000).fit(Xs[:10000], Xs[:10000])
recon = ae.predict(Xs)
err = np.linalg.norm(Xs - recon, axis=1)
print("hidden", hidden, "top5", np.argsort(err)[-5:][::-1].tolist(), "outlier-virheet", np.round(err[-2:], 2), "...", np.round(err[:2], 2))

# Tehdään uusi dataframe, jonne yhdistetään labelit ja häviöt
new_df = pd.DataFrame({
    "rekonstruktiohäviö": np.round(err, 4),
    "label": y.values})

print(new_df.sort_values("rekonstruktiohäviö", ascending=False).head(10))

threshold_95 = np.percentile(err, 95)
threshold_99 = np.percentile(err, 99)

print(f"95. persentiilin kynnysarvo: {threshold_95:.6f}")
print(f"99. persentiilin kynnysarvo: {threshold_99:.6f}")
