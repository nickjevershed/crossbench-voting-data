#%%
import pandas as pd

votes = pd.read_csv('votes.csv')
print(votes.columns)

names = ['Coalition','Australian Labor Party', 'Australian Greens','Dai Le','Andrew Wilkie','Helen Haines','Zali Steggall', 'Kate Chaney', 'Zoe Daniel', 'Monique Ryan', 'Sophie Scamps', 'Kylea Tink', 'Allegra Spender']

def compareAgreement(name1, name2):
    if (name1 == name2):
        return 1
    else:
        temp_df = votes[[name1, name2]]
        # remove missing values
        temp_df = temp_df.dropna()
        temp_df['agree'] = (temp_df[name1] == temp_df[name2]).astype('int')
        temp_df.to_csv('test.csv')
        return sum(temp_df['agree']) / len(temp_df)
    

test = compareAgreement('Coalition', 'Australian Labor Party')
print(test)

matrix = []

for name1 in names:
    row = {"name":name1}
    for name2 in names:
        print(name1, name2)
        result = compareAgreement(name1, name2)
        row[name2] = result
    matrix.append(row)

matrix_df = pd.DataFrame(matrix)
matrix_df.set_index('name', inplace=True)
matrix_df = matrix_df.round(2)

#%%

import plotly.express as px

fig = px.imshow(matrix_df, width=800, height=800, title="Voting agreement in the 47th parliament")
fig.update_xaxes(side="top")
fig.show()

#%%
