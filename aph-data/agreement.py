#%%
import pandas as pd

votes = pd.read_csv('votes.csv')
print(votes.columns)


test = votes[['id', 'title', 'question', 'date', 'aye_votes', 'no_votes', 'mover',
       'mover_party', 'division_type', 'bill_type', 'Australian Labor Party', 'Ms Steggall']]


test = test[test['mover_party'] == 'Australian Labor Party']

katter = votes[pd.notna(votes['Mr Katter'])]
katter_attendance = len(katter.index) / len(votes.index)



#%%
names = ['Coalition','Australian Labor Party', 'Australian Greens', "Mr Gee", 'Ms Le', 'Ms Sharkie', 'Mr Wilkie','Dr Haines','Ms Steggall', 'Ms Chaney', 'Ms Daniel', 'Dr M Ryan', 'Dr Scamps', 'Ms Tink', 'Ms Spender']
# names = ['Coalition','Australian Labor Party', 'Australian Greens', "Mr Broadbent", "Mr Gee", 'Ms Sharkie', "Mr Katter"]
# Optionally filter the type of vote, but this will be moved to the interactive chart

# votes = votes[votes['mover_party'] == 'Australian Labor Party']

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
    

# test = compareAgreement('Coalition', 'Australian Labor Party')
# print(test)

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
matrix_df = matrix_df.round(3)

#%%

import plotly.express as px

fig = px.imshow(matrix_df, width=800, height=800, title="Voting agreement in the 47th parliament")
fig.update_xaxes(side="top")
fig.show()

#%%
