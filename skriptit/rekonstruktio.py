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
    "rekonstruktiohäviö": err,
    "label": y.values})

# Tulostetaan suurimmat rekonstruktiohäviöt
print(new_df.sort_values("rekonstruktiohäviö", ascending=False).head(10))

print(new_df.shape)
new_df.to_csv('pca.csv')

# Tehdään kuvio pääkomponenttianalyysistä. 
plt.figure(figsize=(8,6))

normal = (y == 0)
attack = (y == 1)

# Normaalidata merkitään pallolla
plt.scatter(X_pca[normal, 0],
            X_pca[normal, 1],
            c=err[normal],
            cmap="viridis",
            s=18,
            alpha=0.8,
            marker="o",
            label="Normaali")

# Hyökkäysdata merkitään rastilla
plt.scatter(X_pca[attack, 0],
            X_pca[attack, 1],
            c=err[attack],
            cmap="viridis",
            s=18,
            alpha=0.8,
            marker="x",
            label="Hyökkäys")

plt.colorbar(label="rekonstruktiohäviö")
plt.savefig("pca.png")
plt.legend()
plt.show()

threshold_95 = np.percentile(err, 95)
threshold_99 = np.percentile(err, 99)

print(f"95. persentiilin kynnysarvo: {threshold_95:.6f}")
print(f"99. persentiilin kynnysarvo: {threshold_99:.6f}")
