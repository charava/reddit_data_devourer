import pandas as pd
subreddit_names = ['inventionideas', 'appideas', 'annoyances', 'inventions', 'problems', 'lightbulb']

df = pd.read_csv('identifiedasks.csv')
print(len(df))
df = pd.read_csv('identifiedproblems.csv')
print(len(df))
df = pd.read_csv('identifiedideas.csv')
print(len(df))
df = pd.read_csv('overlapped.csv')
print(len(df))
