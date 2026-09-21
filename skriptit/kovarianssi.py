import pandas as pd

df = pd.read_csv('skaalattu.csv');

kovarianssi_df = df.cov()

kovarianssi_df.to_csv('kovarianssi.csv')

print("Kovarianssi sarakkeittain:\n\n", df.cov())