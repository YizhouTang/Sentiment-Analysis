import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from get_news_data import getNews
from datetime import date,timedelta
import dateutil.parser
import numpy as np
from matplotlib import pyplot as plt

API_KEY = '4182ed52673d404ea2b0a9187f258c0c'

BEGIN_DATE = date.today()- timedelta(30)
BEGIN = BEGIN_DATE.strftime('%Y-%m-%d')
END = date.today().strftime('%Y-%m-%d')
KEYWORD = "Biden"

#nltk.download('vader_lexicon') #only run this once

df = getNews(API_KEY,KEYWORD,BEGIN,END)
df['count'] = 1

analyzer  = SentimentIntensityAnalyzer()

for i in range(len(df)):
    titleSentiment = analyzer.polarity_scores(df['title'][i])['compound']
    descriptionSentiment = analyzer.polarity_scores(df['description'][i])['compound']
    df.loc[i,'sentiment'] = (titleSentiment + descriptionSentiment) / 2
    df.loc[i,'datetime'] = dateutil.parser.parse(df.loc[i,'publishedAt']).strftime('%Y-%m-%d')



df_daily = df.groupby('datetime').mean().loc[:,['sentiment']]
df_daily['numNews'] = df.groupby('datetime').sum().loc[:,'count']

df.to_csv('example_sentiment_scores/News Sentiment - ' + KEYWORD + '.csv')
df_daily.to_csv('example_sentiment_scores/Daily Sentiment - ' + KEYWORD + '.csv')


#Plot graph with 2 y axes
fig, ax1 = plt.subplots()
fig.set_size_inches(15,8)
#Plot bars
ax1.bar(df_daily.index, df_daily['numNews'], alpha=0.3)
ax1.set_xlabel('$Date$')

# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Number of Articles', color='b')
[tl.set_color('b') for tl in ax1.get_yticklabels()]

#Set up ax2 to be the second y axis with x shared
ax2 = ax1.twinx()
#Plot a line
ax2.plot(df_daily.index, df_daily['sentiment'], 'r-')

# Make the y-axis label and tick labels match the line color.
ax2.set_ylabel('Sentiment', color='r')
[tl.set_color('r') for tl in ax2.get_yticklabels()]
fig.autofmt_xdate()
ax1.set_title('Sentiment Analysis - '+ KEYWORD)

plt.show()
plt.savefig('example_plots/Sentiment Analysis - '+ KEYWORD + '.png')