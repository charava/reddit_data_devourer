import praw
import numpy as np
import pandas as pd

dfcheck = pd.read_csv('annoyances.csv')
print(dfcheck.loc[:,'title'])
dfcheck.drop_duplicates(subset=['title'],keep='first',inplace=True)
dfcheck.reset_index(drop=True)
dfcheck.to_csv('annoyances.csv',mode='w',index=False)

print(dfcheck)
