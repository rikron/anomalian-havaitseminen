import pandas as pd

df = pd.read_csv('csv/skaalattu.csv');

kovarianssi_df = df.cov()

kovarianssi_df.to_csv('csv/kovarianssi.csv')

print("Kovarianssi sarakkeittain:\n\n", df.cov())