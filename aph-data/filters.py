#%%
import pandas as pd
votes = pd.read_csv('votes.csv')

#%%

print(list(votes['mover_party'].unique()))

parties = ['Australian Labor Party', 'Australian Greens', 'Independent', 'Coalition', "Katter's Australian Party", 'Centre Alliance']

#%%
print(list(votes['portfolio'].unique()))

portfolios = ['Education', 'Finance', 'Climate Change and Energy', 'Social Services', 'Treasury', 'Women', 'Climate Change, Energy, the Environment and Water', 'Attorney-General', 'Health and Aged Care', 'Skills and Training', 'Home Affairs', 'Communications', 'Infrastructure, Transport, Regional Development, Communications and the Arts', 'Prime Minister and Cabinet', 'Employment and Workplace Relations', 'Defence', 'Agriculture, Fisheries and Forestry', 'Prime Minister', 'National Disability Insurance Scheme', 'Industry, Science and Resources', 'Environment and Water', 'LAMBIE, Sen Jacqui', 'House of Representatives', 'GOSLING, Luke, MP']

