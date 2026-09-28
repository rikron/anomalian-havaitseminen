import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

# Skaalataan standardilla menetelmällä
scaler = StandardScaler()
X = scaler.fit_transform(df)

# Suoritetaan aineistolle PCA ja rekonstruoidaan aineisto.
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
X_reconstructed = pca.inverse_transform(X_pca)

# Selitysasteet
print(pca.explained_variance_ratio_)

# Lasketaan rekonstruktiohäviöt
err = np.linalg.norm(X - X_reconstructed, axis=1)

# Tehdään uusi dataframe, jonne yhdistetään labelit ja häviöt
new_df = pd.DataFrame({
    "indeksi": np.arange(len(err)),
    "rekonstruktiohäviö": err,
    "label": y.values})

# Tulostetaan suurimmat rekonstruktiohäviöt
print(new_df.sort_values("rekonstruktiohäviö", ascending=False).head(10))

print(new_df.shape)
new_df.to_csv('pca.csv')

# Tehdään kuvio pääkomponenttianalyysistä. 
plt.figure(figsize=(8,6))
plt.scatter(X_pca[:, 0], 
            X_pca[:, 1], 
            c=y, 
            cmap='coolwarm', 
            edgecolor='k')
plt.colorbar(label="label")
plt.savefig("pca.png")
plt.show()
