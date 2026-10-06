import numpy as np
import pandas as pd
from pyod.models.lof import LOF
from pyod.models.iforest import IForest

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv');

# Pudotetaan valmiit label arvot ja id, label talteen
y = df['label']
df = df.drop(["id", "attack_cat", "label"], axis=1)
print(df.shape)

# One-hot-koodataan kategoriset arvot ja otetaan sarakkeet talteen
df = pd.get_dummies(df)
columns = df.columns

contamination = 0.1
detectors = {
    "LOF": LOF(contamination=contamination, n_neighbors=500),
    "IForest": IForest(contamination=contamination)
}

all_poikkeavuusarvot = {}

for name, detector in detectors.items():
    detector.fit(df)
    poikkeavuusarvot = detector.decision_function(df)
    all_poikkeavuusarvot[name] = poikkeavuusarvot
    labels = detector.predict(df)
    order = np.argsort(poikkeavuusarvot)[::-1]
    print(name)
    print("Poikkeavuusarvot:", np.round(poikkeavuusarvot, 2))
    print("Labels:", labels)
    print("Suurimmat poikkeavuusarvot:", order[:5])

