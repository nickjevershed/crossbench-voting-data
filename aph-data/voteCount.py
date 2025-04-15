#%%
import pandas as pd
import json

with open('formatted_divisions.json','r') as f:
    divisions = json.load(f)

# divisions = [x for x in divisions if x['divisionId'] == 1944]
votes = []

for division in divisions:

    print("Parsing", division["divisionId"])
    
    df = pd.read_csv(f'division_data_csv/{division["divisionId"]}.csv')
    # df = df[["vote", "member"]]
    # ['Australian Labor Party', 'Liberal National Party of Queensland', 'Liberal Party of Australia', 'Australian Greens', 'The Nationals', 'Independent', 'Centre Alliance']

    print(list(df['Party'].unique()))
    coalition = ['Liberal National Party of Queensland', 'Liberal Party of Australia',  'The Nationals']

    # df['coalition'] = df['Party'].isin(coalition)

    def makeParty(row):
        if row["Party"] in coalition:
            return "Coalition"
        else: 
            return row['Party']

    df['shortParty'] = df.apply(makeParty, axis=1)
    df['count'] = 1

#     coal_votes = df[df['shortParty'] == 'Coalition']
#     coal_votes_count = coal_votes[['count', 'vote']].groupby('vote').sum()
#     coal_votes_count = coal_votes_count.reset_index()

    check_count = None
    def getMajorityVote(party):
        temp_df = df[df['shortParty'] == party]
        if len(temp_df) > 0:
            global check_count
            temp_df_count = temp_df[['count', 'Vote']].groupby('Vote').sum()
            temp_df_count = temp_df_count.reset_index()
            # Sort by highest count
            temp_df_count.sort_values(by=['count'], ascending = False, inplace=True)
            check_count = temp_df_count.copy()
            majorityVote = temp_df_count["Vote"].iloc[0]
            return majorityVote
        else:
            return None

    party_list = ['Coalition', 'Australian Labor Party', 'Australian Greens']

    coal_vote = getMajorityVote('Coalition')
    labor_vote = getMajorityVote('Australian Labor Party')
    greens_vote = getMajorityVote('Australian Greens')
    print("Coalition", coal_vote, "Labor", labor_vote, "Greens", greens_vote)
    print(list(df[df['shortParty'] == 'Independent']['Member']))

    indies = ['Ms Chaney', 'Ms Daniel', 'Dr Haines', 'Dr M Ryan', 'Dr Scamps', 'Ms Spender', 'Ms Steggall', 'Ms Tink', 'Mr Wilkie', 'Ms Le', 'Ms Sharkie', "Mr Katter", "Mr Gee", "Mr Broadbent"]

    results = {
        'id':division['divisionId'],
        'title':division['title'],
        'question':division['question'],
        'date':division['date'],
        'aye_votes':division['ayes'],
        'no_votes':division['noes'],
        'mover':division['mover'],
    }
    
    if 'mover_party' in division:
        results['mover_party'] = division['mover_party']
    else:
        results['mover_party'] = None

    results['division_type'] = division['division_type']

    if division['division_type'] == 'bill':
        results["bill_type"] = division['bill_type']
        results["portfolio"] = division['portfolio']
        results["orig_house"] = division['orig_house']
        results["status"] = division['status']

    results['conscience_vote'] = division['conscienceVote']
    results['Coalition'] = coal_vote
    results['Australian Labor Party'] = labor_vote
    results['Australian Greens'] = greens_vote
    

    for indy in indies:
        if indy in list(df['Member'].unique()):
            results[indy] = df[df['Member'] == indy]['Vote'].iloc[0]
        else:
            results[indy] = None

    votes.append(results)

vote_df = pd.DataFrame(votes)

import csv 

with open("politicians.csv", mode="r") as file:
    reader = csv.DictReader(file)
    politicians = {row["Name"]: row["Party"] for row in reader}
    file.seek(0)
    politicians2 = {row["Name"]: row["Party2"] for row in reader}

vote_df['mover_party2'] = vote_df['mover'].map(politicians2)
vote_df['mover_party'] = vote_df['mover'].map(politicians)

div_types = {"bill":"Bill", "procedural":"Procedural"}

vote_df['division_type'] = vote_df['division_type'].map(div_types)
# df.loc[df['dollars_spent'] > 0, 'purchase'] = 1

# Merge some portfolio names

vote_df.loc[vote_df['portfolio'] == 'Climate Change and Energy', 'portfolio'] = 'Climate Change, Energy, the Environment and Water'

vote_df.loc[vote_df['portfolio'] == 'Environment and Water', 'portfolio'] = 'Climate Change, Energy, the Environment and Water'

vote_df.to_csv('votes.csv', index=False)
vote_df.to_csv('../voting-heatmap/src/assets/votes.csv', index=False)