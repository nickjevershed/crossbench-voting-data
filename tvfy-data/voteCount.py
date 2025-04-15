#%%
import pandas as pd
import json
import scraperwiki

divisions = scraperwiki.sqlite.select("* from divisions")

votes = []

for division in divisions:

    print("Parsing", division["id"])
    with open(f"division_data/{division['id']}.json") as f:  
        data = json.load(f)

    vote_record = []

    for vote in data["votes"]:
        new_row = {
            "vote": vote["vote"],
            "name": vote["member"]["first_name"] + " " + vote["member"]["last_name"],
            "electorate": vote["member"]["electorate"],
            "party": vote["member"]["party"],
            "id": vote["member"]["person"]["id"]
        }

        vote_record.append(new_row)

    df = pd.DataFrame(vote_record)
    # df = df[["vote", "member"]]

    print(list(df['party'].unique()))
    coalition = ['Liberal Party', 'National Party', 'Liberal National Party']

    # df['coalition'] = df['party'].isin(coalition)

    def makeParty(row):
        if row["party"] in coalition:
            return "Coalition"
        else: 
            return row['party']

    df['shortParty'] = df.apply(makeParty, axis=1)
    df['count'] = 1

    coal_votes = df[df['shortParty'] == 'Coalition']
    coal_votes_count = coal_votes[['count', 'vote']].groupby('vote').sum()
    coal_votes_count = coal_votes_count.reset_index()

    def getMajorityVote(party):
        temp_df = df[df['shortParty'] == party]
        if len(temp_df) > 0:
            
            temp_df_count = temp_df[['count', 'vote']].groupby('vote').sum()
            temp_df_count = temp_df.reset_index()
            # Sort by highest count
            temp_df_count.sort_values(by=['count'], ascending = False, inplace=True)
            majorityVote = temp_df_count["vote"].iloc[0]
            return majorityVote
        else:
            return None

    party_list = ['Coalition', 'Australian Labor Party', 'Australian Greens']

    coal_vote = getMajorityVote('Coalition')
    labor_vote = getMajorityVote('Australian Labor Party')
    greens_vote = getMajorityVote('Australian Greens')

    indies = ['Helen Haines', 'Zali Steggall', 'Andrew Wilkie', 'Kate Chaney', 'Zoe Daniel', 'Monique Ryan', 'Sophie Scamps', 'Kylea Tink', 'Allegra Spender', 'Dai Le']

    results = {
        'id':data['id'],
        'name':data['name'],
        'date':data['date'],
        'aye_votes':data['aye_votes'],
        'no_votes':data['no_votes'],
        'Coalition': coal_vote,
        'Australian Labor Party': labor_vote,
        'Australian Greens': greens_vote
    }

    for indy in indies:
        if indy in list(df['name'].unique()):
            results[indy] = df[df['name'] == indy]['vote'].iloc[0]
        else:
            results[indy] = None

    votes.append(results)

vote_df = pd.DataFrame(votes)
vote_df.to_csv('votes.csv', index=False)



