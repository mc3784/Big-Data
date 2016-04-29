
import numpy as np
import pandas as pd
import sys
import json
import datetime as dt

fileName = 'sample3.csv'
try:
	fileName = sys.argv[1]
except:
	print "The program require a the data file name as an argument"
	sys.exit()
#Read data from file and split it in a list neighborDf, containing one dataframe for each neighbourhood
df = pd.read_csv(fileName, parse_dates=[0], sep=',')
df=df.sort(['neighbourhood','Date'])
gb = df.groupby('neighbourhood')    
neighborDf=[gb.get_group(x) for x in gb.groups]


def sum_week_after(row):
    return df['count'].iloc[row['today_index']+1:row['end_week_after']].sum()
def sum_week_before(row):
    return df['count'].iloc[row['start_week_before']:row['today_index']].sum()

weekBefore={}
weekAfter={}

#Loop for each df and append in the two dictionary the aggragation count for the week before and the week after a given day.

for df in neighborDf:
    neighborIndex=df['neighbourhood'].unique()[0]
    newIndex=range(len(df))
    df=df.set_index([newIndex])
    df['today_index'] = df.index
    start_dates = df['Date'] - pd.Timedelta(days=8)
    df['start_week_before'] = df['Date'].values.searchsorted(start_dates, side='right')
    end_date = df['Date'] + pd.Timedelta(days=8)
    df['end_week_after'] = df['Date'].values.searchsorted(end_date, side='left')
    df['count_week_after'] = df.apply(sum_week_after, axis=1)
    df['count_week_before'] = df.apply(sum_week_before, axis=1)
    df['Date']=df['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    dfToSave=df[['Date','count_week_before','count_week_after']]
    weekBefore[neighborIndex]=dfToSave.set_index('Date')['count_week_before'].to_dict()
    weekAfter[neighborIndex]= dfToSave.set_index('Date')['count_week_after'].to_dict()

with open('weekBefore.txt', 'w+') as f:
    json.dump(weekBefore, f)

with open('weekAfter.txt', 'w+') as f:
    json.dump(weekAfter, f)

print "Dictionary for the week before: "
print weekBefore
print "Dictionary for the week after: "
print weekAfter




