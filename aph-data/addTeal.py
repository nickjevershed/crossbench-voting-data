#%%
import pandas as pd
import csv

with open("politicians.csv", mode="r") as file:
    reader = csv.DictReader(file)
    politicians2 = {row["Name"]: row["Party2"] for row in reader}

votes = pd.read_csv('votes.csv')

votes['mover_party2'] = votes['mover'].map(politicians2)


