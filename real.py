import praw
import numpy as np
import pandas as pd
from os.path import exists
#import cron...automate a weekly schedule for scraping
#octaparse, amazon lambda

#https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
reddit = praw.Reddit(client_id='izBlAjZ7nSAT62DPxU2thw', client_secret='9OwPwh_axISvTOZwWZN9g66im-C-AA', user_agent='Scraper2')

#reddit = praw.Reddit(client_id='9FOPiLyp8H5GnfCWa2O2ZA', client_secret='FlwV13e7uYP_O778lSZftNDJ0pCqqw', user_agent='WebScraping')
subreddit_names = ['inventionideas', 'appideas', 'annoyances', 'inventions', 'problems', 'lightbulb']
#maybe dont have lightbulb idk


#just delete the phrase from the row
unnecessary_phrases = ['hi','hello','thanks','thx',
'ty','tx','dear community','i am looking for',':)']

#this is a sign to delete the entire post/row
personal_phrases = ['my idea','my app','my invention','i\'ve got an idea',
'i\'ve got an app','i\'ve got an invention','i\'ve been thinking',
'i\'ve got this','my product','need your','feedback',]



#number of loops for the different functions
FIRSTSCRAPEMAXPOSTS = 20
LOOPMAXPOSTS = 20
MAINFILE = 'first.csv'



#first scrape -- creating the first ever file
def firstScrape():
    for name in subreddit_names: #only want to do this once
        filename = name + '.csv'
        subreddit = reddit.subreddit(name)
        #sorting into individual csv files based on subreddit
        postList = []
        for post in subreddit.new(limit=FIRSTSCRAPEMAXPOSTS):
            postList.append([post.title, post.score, post.selftext, post.id])
        df = pd.DataFrame(postList, columns=['title','score','body','id'])

        if exists(filename):
            no_index(filename)
        else:
            df.to_csv(filename,mode='w',header=True, index=False)     #creating individual csv
            no_index(filename)

        if exists(MAINFILE):
            no_index(MAINFILE)
        else:
            df.to_csv(MAINFILE,mode='w',header=True,index=False)     #creating an amalgamated csv file
            no_index(MAINFILE)


#function to scrape once file has already been created
def loopScrape():
    for name in subreddit_names:
        filename = name + '.csv'
        subreddit = reddit.subreddit(name)
        #sorting into individual csv files based on subreddit
        postList = []
        for post in subreddit.new(limit=LOOPMAXPOSTS):
            #df = pd.read_csv(filename)
            #if post.title not in df['title']:
            postList.append([post.title, post.score, post.selftext, post.id])

        df = pd.DataFrame(postList, columns=['title','score','body','id'])
        df.to_csv(filename,mode='a', header=False, index=False)  #creating individual csv
        df.to_csv(MAINFILE,mode='a', header=False, index=False) #creating an amalgamated csv file


def no_dupes(filename):
    df = pd.read_csv(filename)
    df.drop_duplicates(subset=['title'],keep='first',inplace=True)
    df.to_csv(filename, index=False)

#deleting index columns to prevent index=False from being true somehow
def no_index(filename):
    df = pd.read_csv(filename)
    column_headers = df.columns.values
    for number in range(len(column_headers)):
        name = column_headers[number]
        loweredname = name.lower()
        if 'unnamed' in loweredname:
            df.drop(labels=name, axis=1,inplace=True) #used to be df =   and had inplace False
    df.to_csv(filename, index=False)


# copy dfcheck2 and then when personal prhase found in dfcheck2, modify dfcheck3
#cleaning for the first.csv file
def clean_data(filename):
    dfcheck2 = pd.read_csv(filename)
    no_dupes(filename)
    no_index(filename)


    #replacing special characters
    dfcheck2=dfcheck2.replace('\*','',regex=True)
    dfcheck2=dfcheck2.replace('&#x200B;','',regex=True) #RIGHT NOW NOT DELETING

    #once replacing special characters has happened
    dfcheck3 = dfcheck2.copy(deep=True)
    cleaned_file = 'new' + filename

    # MIGHT JUST BE A PROBLEM WITH INVENTIONS.CSV
    #deleting rows with personal phrases in them
    for row in range(len(dfcheck2)):
        row_title = dfcheck2.loc[row, 'title']
        row_body = dfcheck2.loc[row,'body']
        another = True

        while another == True:
            for phrase in personal_phrases:
                phrase = phrase.lower()

                if isinstance(row_title, str):
                    row_title = row_title.lower()
                    if phrase in row_title:
                        print('found in row title')
                        print('filename = ' + filename + '  row = ' + str(row))
                        dfcheck3.drop(labels=row,axis=0, inplace=True)
                        another = False

                    elif isinstance(row_body, str):
                        row_body = row_body.lower()
                        if phrase in row_body:
                            print('found in body')
                            print('filename = ' + filename + '  row = ' + str(row))
                            dfcheck3.drop(labels=row,axis=0,inplace=True)
                            another = False


    dfcheck3.to_csv(cleaned_file,mode='w',index=False)
    no_index(cleaned_file)
    no_dupes(cleaned_file)

    no_index(filename)
    no_dupes(filename)

'''
    for row in range(len(dfcheck2)):
        print('1')
        for phrase in personal_phrases:
            phrase = phrase.lower()
            row_title = dfcheck2.loc[row, 'title']
            row_body = dfcheck2.loc[row,'body']

            if isinstance(row_title, str):
                row_title = row_title.lower()
                if phrase in row_title:
                    print('found in row title')
                    print('filename = ' + filename + '  row = ' + str(row))
                    dfcheck3.drop(labels=row,axis=0, inplace=True)

                elif isinstance(row_body, str):
                    print('2')
                    row_body = row_body.lower()
                    if phrase in row_body:
                        print('3')
                        print('found in body')
                        print('filename = ' + filename + '  row = ' + str(row))
                        dfcheck3.drop(labels=row,axis=0,inplace=True)

    cleaned_file = 'new' + filename
    dfcheck3.to_csv(('new' + filename),mode='w',index=False)
    no_index(cleaned_file)
    no_dupes(cleaned_file)
    #check here

    no_index(filename)
    no_dupes(filename)
'''


    #look at relevance algorithm， google?


#-------------------------

# THE ACTUAL SCRAPING

#firstScrape()
#loopScrape()

no_dupes(MAINFILE)
no_index(MAINFILE)

for name in subreddit_names:
    filename = name + '.csv'
    no_dupes(filename)
    no_index(filename)

'''
#CLEANING DATA
for name in subreddit_names:
    filename = name + '.csv'
    no_dupes(filename)
    no_index(filename)
    clean_data(filename)
'''

clean_data(MAINFILE)

#add more personal personal_phrases
#delete unneded phrases, inplace=True
#make list of innapropro words and replace them
#make sure its replacing unnecessary phrases cuz its no, adde emojis to unnecessary phrase list
#AND clean stop words, but append to new file, perhaps combine this step with dfcheck3
#fix spelling errors
#mech turk

#READ ABT RELEVANCE SEARCH ML ALGORITHMS AND NLP
#Clean inappropriate, swear words (github cleaner code)
# https://github.com/vzhou842/profanity-check/tree/master/profanity_check
#replaced "fucked" "messed"

#deleting stuff around relationships?



#sorting into categories using text classification like ckimate change, health for
#displaying on the website



'''
QUESTIONS:
Why does it take so long to scrape in my program? Is this literally just the scraping
or is my code just not efficient?

scraping on a schedule? run on a server and import datetime to scrape every week
can i have my code run and scrape every week

should i eventually just drop the indiviudal files

THOUGHTS:
for the actual front end website, create a feature for the mod
to delete posts easily by clicking an x on the interface
'''
