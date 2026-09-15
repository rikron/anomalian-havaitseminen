import pandas as pd
import numpy as np

df = pd.read_csv('aineisto/CSV Files/Training and Testing Sets/UNSW_NB15_testing-set.csv');
print("Datan muoto:\n\n", df.shape);
print("")
print("--------------------------------------")
print("")
print("Puuttuvat arvot:\n\n", df.isnull().sum());
print("")
print("--------------------------------------")
print("")

numeeriset = df.select_dtypes(include=np.number)

print("Minimit sarakkeittain:\n\n", numeeriset.min())
print("")
print("--------------------------------------")
print("")
print("Maksimit sarakkeittain:\n\n", numeeriset.max())