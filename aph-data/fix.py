#%% Fuck the Index
import pandas as pd
import os

files = os.listdir('division_data')

for file in files:
    df = pd.read_csv(f'division_data/{file}', usecols=['Member','Party','Vote'])
    df.to_csv(f'division_data/{file}', index=False)