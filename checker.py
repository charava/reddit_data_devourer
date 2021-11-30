import praw
import numpy as np
import pandas as pd

dfcheck = pd.read_csv('annoyances.csv')



for indexNumber in range(len(dfcheck.loc[:,'title'])):
    print('INDEX IS ' + str(indexNumber))
    first = dfcheck.loc[indexNumber,'title']
    print(first)
    print()
    for numberAbove in range(1, (len(dfcheck.loc[:,'title']) - indexNumber)):
        secondIndexNumber = indexNumber + numberAbove
        second = dfcheck.loc[secondIndexNumber,'title']
        print(second)
        if first == second:
            print('its owkring')
            #its deleting everything up to the second index
            print(indexNumber)
            dfcheck.drop(index=indexNumber,inplace=True)
            dfcheck.to_csv('checkingthe.csv',mode='w',index=True)

    print("its jumpin")
    print(dfcheck.loc[:,'title'])

            #delete
