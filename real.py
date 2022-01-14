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
# MY IDEA SEEMS TO GO BOTH WAYS...SOME CASES ACTUALLY ARENT PERSONAL


problem_keywords = ['problem', 'issue','bad','difficult','can\'t','trouble','hard','not good']
#need to identify people asking a # QUESTION:

idea_keywords = ['idea','solution','solve','improve','better','improve','fix','what if','propos',]
#could aslo sort from actual subreddit like all the app ideas and invention ideas
#AppIdeas
#inventionideas

ask_keywords = ['?','can you','need','ask','want','please']
not_ask_keywords = [] #if this is in an ask phrase, then it cant be an ask phrase and must be deleted




#number of loops for the different functions
FIRSTSCRAPEMAXPOSTS = 10
LOOPMAXPOSTS = 90
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
def cleanData(filename):
    dfcheck2 = pd.read_csv(filename)
    no_dupes(filename)
    no_index(filename)


    #replacing special characters
    dfcheck2=dfcheck2.replace('\*','',regex=True)
    dfcheck2=dfcheck2.replace('&#x200B;','',regex=True) #RIGHT NOW NOT DELETING


    # clean bad words

    #taking out unnecesary phrases



    #once replacing special characters has happened
    dfcheck3 = dfcheck2.copy(deep=True)
    cleaned_file = 'clean' + filename


    dropped_stuff = []

    #deleting rows with personal phrases in them
    for row in range(len(dfcheck2)):
        row_title = dfcheck2.loc[row, 'title']
        row_body = dfcheck2.loc[row,'body']

        for phrase in personal_phrases:
            phrase = phrase.lower()

            if isinstance(row_title, str):
                row_title = row_title.lower()
                if phrase in row_title:
                    #print('found in row title')
                    #print('filename = ' + filename + '  row = ' + str(row))
                    dfcheck3.drop(labels=row,axis=0, inplace=True)
                    dropped_stuff.append(dfcheck2.loc[row]) #seeing what is NOT on newfirst
                    break

                elif isinstance(row_body, str):
                    row_body = row_body.lower()
                    if phrase in row_body:
                        #print('found in body')
                        #print('filename = ' + filename + '  row = ' + str(row))
                        dfcheck3.drop(labels=row,axis=0,inplace=True)
                        dropped_stuff.append(dfcheck2.loc[row]) #seeing what is NOT on newfirst
                        break


    dfcheck3.to_csv(cleaned_file,mode='w',index=False)
    no_index(cleaned_file)
    no_dupes(cleaned_file)


    df = pd.DataFrame(dropped_stuff, columns=['title','score','body','id'])
    if exists('droppedstuff.csv'):
        df.to_csv('droppedstuff.csv',mode='a', header=False, index=False)
    else:
        df.to_csv('droppedstuff.csv',mode='w', header=True, index=False)
    no_dupes('droppedstuff.csv')
    no_index('droppedstuff.csv')


    no_index(filename)
    no_dupes(filename)




def findProblems(filename): #eh take out...too ambiguous to just look for key words
    check = pd.read_csv(filename)
    no_dupes(filename)
    no_index(filename)

    unsorted = []
    identifiedList = []
    for row in range(len(check)):
        row_title = check.loc[row, 'title']
        row_body = check.loc[row,'body']

        for phrase in problem_keywords:
            phrase = phrase.lower()

            if isinstance(row_title, str):
                row_title = row_title.lower()
                if phrase in row_title:
                    identifiedList.append(check.loc[row])
                    break

                elif isinstance(row_body, str):
                    row_body = row_body.lower()
                    if phrase in row_body:
                        identifiedList.append(check.loc[row])
                        break
                    else:
                        unsorted.append(check.loc[row])
                        break

                else:
                    unsorted.append(check.loc[row])



    df = pd.DataFrame(identifiedList, columns=['title','score','body','id'])
    if exists('identifiedproblems.csv'):
        df.to_csv('identifiedproblems.csv',mode='a', header=False, index=False)
    else:
        df.to_csv('identifiedproblems.csv',mode='w', header=True, index=False)  #to get a header initially
    no_dupes('identifiedproblems.csv')
    no_index('identifiedproblems.csv')


    anotherdf = pd.DataFrame(identifiedList, columns=['title','score','body','id'])
    if exists('unsorted.csv'):
        anotherdf.to_csv('unsorted.csv',mode='a', header=False, index=False)
    else:
        anotherdf.to_csv('unsorted.csv',mode='w', header=True, index=False)  #to get a header initially
    no_dupes('unsorted.csv')
    no_index('unsorted.csv')



def findIdeas(filename): #eh take out...too ambiguous to just look for key words
    check = pd.read_csv(filename)
    no_dupes(filename)
    no_index(filename)


    identifiedList = []
    for row in range(len(check)):
        row_title = check.loc[row, 'title']
        row_body = check.loc[row,'body']

        for phrase in idea_keywords:
            phrase = phrase.lower()

            if isinstance(row_title, str):
                row_title = row_title.lower()
                if phrase in row_title:
                    identifiedList.append(check.loc[row])
                    break

                elif isinstance(row_body, str):
                    row_body = row_body.lower()
                    if phrase in row_body:
                        identifiedList.append(check.loc[row])
                        break


    df = pd.DataFrame(identifiedList, columns=['title','score','body','id'])
    if exists('identifiedideas.csv'):
        df.to_csv('identifiedideas.csv',mode='a', header=False, index=False)
    else:
        df.to_csv('identifiedideas.csv',mode='w', header=True, index=False)  #to get a header initially
    no_dupes('identifiedideas.csv')
    no_index('identifiedideas.csv')



def findAsks(filename): #eh take out...too ambiguous to just look for key words
    check = pd.read_csv(filename)
    no_dupes(filename)
    no_index(filename)


    identifiedList = []
    for row in range(len(check)):
        row_title = check.loc[row, 'title']
        row_body = check.loc[row,'body']

        for phrase in ask_keywords:
            phrase = phrase.lower()

            if isinstance(row_title, str):
                row_title = row_title.lower()
                if phrase in row_title:
                    identifiedList.append(check.loc[row])
                    break

                elif isinstance(row_body, str):
                    row_body = row_body.lower()
                    if phrase in row_body:
                        identifiedList.append(check.loc[row])
                        break


    df = pd.DataFrame(identifiedList, columns=['title','score','body','id'])
    if exists('identifiedasks.csv'):
        df.to_csv('identifiedasks.csv',mode='a', header=False, index=False)
    else:
        df.to_csv('identifiedasks.csv',mode='w', header=True, index=False)  #to get a header initially
    no_dupes('identifiedasks.csv')
    no_index('identifiedasks.csv')



def overlapped():   #overlapped is consolidating all the posts that fall under all three categories: problem, idea, and ask
    problems = pd.read_csv('identifiedproblems.csv')
    ideas = pd.read_csv('identifiedideas.csv')
    asks = pd.read_csv('identifiedasks.csv')

    identifiedList = []

    for problems_row in range(len(problems)):
        problems_post = problems.loc[problems_row, 'title']

        for ideas_row in range(len(ideas)):
            ideas_post = ideas.loc[ideas_row, 'title']

            for asks_row in range(len(ideas)):
                asks_post  = asks.loc[asks_row, 'title']

                if problems_post == ideas_post:
                    identifiedList.append(ideas.loc[ideas_row])
                    break
                elif asks_post == problems_post:
                    identifiedList.append(ideas.loc[problems_row])
                    break
                elif asks_post == ideas_post:
                    identifiedList.append(ideas.loc[asks_row])
                    break

    #not efficient code, copies thousands of repeats to csv then deletes dupes at the very end

    df = pd.DataFrame(identifiedList, columns=['title','score','body','id'])
    if exists('overlapped.csv'):
        df.to_csv('overlapped.csv',mode='a', header=False, index=False)
    else:
        df.to_csv('overlapped.csv',mode='w', header=True, index=False)  #to get a header initially

    no_dupes('overlapped.csv')
    no_index('overlapped.csv')



#-------------------------

# THE ACTUAL SCRAPING
firstScrape()
loopScrape()

no_dupes(MAINFILE)
no_index(MAINFILE)

for name in subreddit_names:
    filename = name + '.csv'
    no_dupes(filename)
    no_index(filename)


#CLEANING DATA
for name in subreddit_names:
    filename = name + '.csv'
    cleanData(filename)

cleanData(MAINFILE)

findProblems(MAINFILE) #eh take out
findIdeas(MAINFILE)
findAsks(MAINFILE)
overlapped()

#add more personal personal_phrases
#delete unneded phrases, inplace=True
#make list of innapropro words and replace them
#make sure its replacing unnecessary phrases cuz its no, adde emojis to unnecessary phrase list
#AND clean stop words, but append to new file, perhaps combine this step with dfcheck3
#fix spelling errors

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


CSV KEY:
dropped stuff = stuff that is not cleandata() thought had a personal phrase and shouldnt
be accounted for

first, inventionideas, lightbulb...etc = the original scrape straight from reddit

newannoyances, newfirst...etc = went through cleandata() and is everything that didn't
have personal phrases

identifiedasks = sorted "asks" or need statements from the new___ files
identifiedproblems = sorted "problem" statements from new____ files
identifiedideas = sorted "idea" statements from new___ files

overlapped = all the posts that got sorted into 2 or more categories: ask and a problem, idea and a problem, problem and ask

stopwords = so far not used, needed though if want to strip down strings to key words ONLY

unsorted = stuff from new___ that didn't qualify as an ask, idea, or problem based on find___ functions
'''
