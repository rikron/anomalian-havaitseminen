import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

df = df.sample(
    n=10000,
    random_state=42
)

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

X = df.astype(float)

# Skaalataan standardilla menetelmällä
scaler = StandardScaler()
X = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

eps = 1
labels = DBSCAN(eps=eps, min_samples=2).fit_predict(X_pca)

print("labelit:", labels.tolist())
print("kohina:", np.where(labels == -1)[0].tolist())
plt.scatter(X_pca[:,0], X_pca[:,1], c=labels, cmap="tab10", s=80)
plt.scatter(X_pca[labels==-1,0], X_pca[labels==-1,1], facecolors="none", edgecolors="red", s=180)
plt.title(f"DBSCAN eps={eps}")
plt.savefig("kuvat/klusterointi.png")
plt.show()