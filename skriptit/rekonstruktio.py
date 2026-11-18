import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

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
    "label": y.values}, index=df.index+1)

# Tulostetaan suurimmat rekonstruktiohäviöt
print(new_df.sort_values("rekonstruktiohäviö", ascending=False).head(10))

print(new_df.shape)
new_df.to_csv('csv/pca.csv')

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
plt.savefig("kuvat/pca.png")
plt.legend()
plt.show()

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
