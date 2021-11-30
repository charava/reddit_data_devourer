import praw
import numpy as np
import pandas as pd
from os.path import exists
#import cron...automate a weekly schedule for scraping

reddit = praw.Reddit(client_id='9FOPiLyp8H5GnfCWa2O2ZA', client_secret='FlwV13e7uYP_O778lSZftNDJ0pCqqw', user_agent='WebScraping')
subreddit_names = ['inventionideas', 'appideas', 'annoyances', 'inventions', 'problems', 'lightbulb']
#maybe dont have lightbulb idk

#number of loops for the different functions
FIRSTSCRAPEMAXPOSTS = 20
LOOPMAXPOSTS = 20
MAINFILE = 'first.csv'



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
        df.to_csv(filename,mode='w',header=True, index=False)     #creating individual csv
        df.to_csv(MAINFILE,mode='w',header=True,index=False)     #creating an amalgamated csv file


def loopScrape():
    for x in range(2):#loop scrape...change to scraping on weekly basis
        for name in subreddit_names:
            filename = name + '.csv'
            subreddit = reddit.subreddit(name)
            #sorting into individual csv files based on subreddit
            postList = []
            for post in subreddit.new(limit=LOOPMAXPOSTS):
                df = pd.read_csv(filename)
                if post.title not in df:
                    postList.append([post.title, post.score, post.selftext, post.id])

            df = pd.DataFrame(postList, columns=['title','score','body','id'])
            df.reset_index() #if the file has already been looped before, reset the index
            df.to_csv(filename,mode='a', header=False, index=False)  #creating individual csv
            df.to_csv(MAINFILE,mode='a', header=False, index=False) #creating an amalgamated csv file



#ITS NOT WORKING AND ADDING DOUBLE FOR EVERY NEW LOOP
def addIndex(): #to give it an index that is not repeated with every loop

    for name in subreddit_names: #making sure only one axis for each individual file
        filename = name + '.csv'
        read = pd.read_csv(filename)
        if (read.loc[:,'Unnamed']) != []:
            read.drop(axis='Unnamed', inplace=True)
            read.to_csv(filename)

        df = pd.read_csv(filename)
        df.reset_index()
        df.to_csv(filename,mode='w',index=False)


    df2 = pd.read_csv(MAINFILE) #making sure only one axis for main file
    if df2.loc[:,'Unnamed'] != []:
        df2.drop(axis='Unnamed', inplace=True)
    df2.reset_index()
    df2.to_csv(MAINFILE,mode='w',index=False)




# all the scraping
for name in subreddit_names:
    filename = name + '.csv'
    if (exists(filename)): #if the file exists already, then only move on to appending new posts
        pass
    else:
        firstScrape() #if file doesn't exist already, first create the file and don't append
loopScrape()


#dropping duplicates
for name in subreddit_names:
    filename = name + '.csv'
    dfcheck = pd.read_csv(filename)
    dfcheck.drop_duplicates(subset=['title'],keep='first',inplace=True)
    dfcheck.to_csv(filename,mode='w',index=False)
dfcheck2 = pd.read_csv(MAINFILE)
dfcheck2.drop_duplicates(subset=['title'],keep='first',inplace=True)
dfcheck2.to_csv(MAINFILE,mode='w',index=False)


#adding an index
#addIndex() #right now its kinda Unnecessary


#Clean data from special characters
# emojis, &#x200B;, "hi i've got an", "hello", "thanks", thx, ty, "dear community"
# just wanted to share


#should i eventually just drop the individual files


#Clean inappropriate, swear words (github cleaner code)
# https://github.com/vzhou842/profanity-check/tree/master/profanity_check
#replaced "fucked" "messed"
#sentiment anaylsis?

#summarize the data
#fix spelling errors

# deleting the irrelevent, innapropriate data: use crowd working (hire people to sort the data)
# or you can try to implement a sentiment model...which is sketchy

#deleting stuff around relationship



'''
QUESTIONS:
Why does it take so long to scrape in my program? Is this literally just the scraping
or is my code just not efficient?

scraping on a schedule? run on a server and import datetime to scrape every week
can i have my code run and scrape every week
'''
