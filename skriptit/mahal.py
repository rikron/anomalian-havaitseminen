import pandas as pd
import numpy as np
import scipy

df = pd.read_csv('skaalattu.csv');

numeeriset = df.select_dtypes(include=np.number)

def mahalanobis(df):
    cov = df.cov().values
    inv_cov = np.linalg.inv(cov)
    mean = df.mean().values
    scores = []
    values = df.values
    for i in range(values.shape[0]):
        score = scipy.spatial.distance.mahalanobis(mean, values[i], inv_cov)
        scores.append(score)
    return pd.Series(data=scores, index=df.index)

valitut = numeeriset[["dur", "rate", "sbytes", "dbytes"]]

mahal = mahalanobis(valitut)
print("Mahalanobis:\n\n", mahal)
mahal.to_csv('mahalanobis.csv')

print("Minimit:\n\n", mahal.sort_values().head(5))
print("")
print("--------------------------------------")
print("")
print("Maksimit:\n\n", mahal.sort_values(ascending=False).head(5))