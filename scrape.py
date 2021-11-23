import praw
import numpy as np
import pandas as pd


reddit = praw.Reddit(client_id='9FOPiLyp8H5GnfCWa2O2ZA', client_secret='FlwV13e7uYP_O778lSZftNDJ0pCqqw', user_agent='WebScraping')


subreddit_category = 'ideas' #this variable doesn't actually do anything except name the file
#TOO DOOOOOOOscrape description of climate change for more subreddits and apply to list
print(reddit.subreddit(subreddit_category).description)
subreddit_names = ['ideas', 'inventionideas', 'appideas']
num_of_posts = 10

post_list = []
for name in range(len(subreddit_names)):
    access_subreddit = reddit.subreddit(subreddit_names[name])

    for post in access_subreddit.top(limit=num_of_posts):
        post_list.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

post_list = pd.DataFrame(post_list,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

filename = subreddit_category + '_posts.csv'
post_list.to_csv(filename, index=False)

#create a loop and if there are other subreddits in description, check them out too


'''
ONLY IF I NEED SUBREDDIT DESCRIPTIONS
#writing description of the subreddit to another csv file
description = test_subreddit.description
f = open('subreddit_description.txt', 'w') #interesting to note that the description offers other subreddits to look into
f.write(description)
f.close()
'''





#to learn more about read_csv
#https://towardsdatascience.com/pandas-dataframe-playing-with-csv-files-944225d19ff

print('done')
