import pandas as pd
subreddit_names = ['inventionideas', 'appideas', 'annoyances', 'inventions', 'problems', 'lightbulb']

def no_dupes(filename):
    df = pd.read_csv(filename)
    df.drop_duplicates(subset=['title'],keep='first',inplace=True)
    df.to_csv(filename)

#deleting index columns to prevent index=False from being true somehow
def no_index(filename):
    df = pd.read_csv(filename)
    column_headers = df.columns.values
    for number in range(len(column_headers)):
        name = column_headers[number]
        loweredname = name.lower()
        if 'unnamed' in loweredname:
            df.drop(labels=name, axis=1,inplace=True)
    df.to_csv(filename, index=False)



for name in subreddit_names:
    filename = name + '.csv'
    no_dupes(filename)
    no_index(filename)
df = pd.read_csv('first.csv')
print(df.loc[160,'title'])
