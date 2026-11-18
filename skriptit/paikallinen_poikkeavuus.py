import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

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

lof = LocalOutlierFactor(n_neighbors=500)
lof.fit_predict(X_pca)
lof_poikkeavuusarvot = -lof.negative_outlier_factor_
print("LOF top", int(np.argmax(lof_poikkeavuusarvot)), "LOF", np.round(lof_poikkeavuusarvot, 2))

df1 = pd.DataFrame(lof_poikkeavuusarvot, columns=['lof poikkeavuusarvo'])
print("Maksimit:\n\n", df1.sort_values(ascending=False, by='lof poikkeavuusarvo').head(5))
df1.to_csv('csv/lof.csv')