import praw
import numpy as np
import pandas as pd
from os.path import exists

reddit = praw.Reddit(client_id='9FOPiLyp8H5GnfCWa2O2ZA', client_secret='FlwV13e7uYP_O778lSZftNDJ0pCqqw', user_agent='WebScraping')
subreddit_names = ['inventionideas', 'appideas', 'annoyances', 'inventions', 'problems', 'lightbulb']
#maybe dont have lightbulb idk

#number of loops for the different functions
FIRSTSCRAPEMAXPOSTS = 5
LOOPMAXPOSTS = 5


#issue is the no duplicates is only deleting one of the three scrapes
def eachFile_noDuplicates():
    for name in subreddit_names:
        filename = name + '.csv'
        df = pd.read_csv(filename)
        df.drop_duplicates(subset=['title'],keep='first', inplace=True)
        print('lel')

def noDuplicates(filename):
    df = pd.read_csv(filename)
    df.drop_duplicates(subset=['title'],keep='first',inplace=True)
    print('yo')

#first scrape
def firstScrape():
    for name in subreddit_names: #only want to do this once
        filename = name + '.csv'
        subreddit = reddit.subreddit(name)
        #sorting into individual csv files based on subreddit
        postList = []
        for post in subreddit.new(limit=FIRSTSCRAPEMAXPOSTS):
            postList.append([post.title, post.score, post.selftext, post.id])
        df = pd.DataFrame(postList, columns=['title','score','body','id'])
        df.to_csv(filename,mode='w',header=True, index=False)
        df.to_csv('first.csv',mode='w',header=True,index=False)


def loopScrape():
    for x in range(2):#loop scrape...change to scraping on weekly basis
        for name in subreddit_names:
            filename = name + '.csv'
            subreddit = reddit.subreddit(name)
            #sorting into individual csv files based on subreddit
            postList = []
            for post in subreddit.new(limit=LOOPMAXPOSTS):
                postList.append([post.title, post.score, post.selftext, post.id])
            df = pd.DataFrame(postList, columns=['title','score','body','id'])
            df.to_csv(filename,mode='a', header=False, index=False)
            df.to_csv('first.csv',mode='a',header=False,index=False)


for name in subreddit_names:
    filename = name + '.csv'
    if (exists(filename)): #if the file exists
        pass
    else:
        firstScrape()
loopScrape()

#DROPPING DUPES AREN'T WORKING
#dropping the duplicates in each of the sliced files
eachFile_noDuplicates()
#eliminatng duplicates in consolidated file
noDuplicates('first.csv')




#append all seperate into  one csv file

#Clean data from special characters

#Clean inappropriate, swear words (github cleaner code)



'''
QUESTIONS:
Why does it take so long to scrape in my program? Is this literally just the scraping
or is my code just not efficient?
'''
