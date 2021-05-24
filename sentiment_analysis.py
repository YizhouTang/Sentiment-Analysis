import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from get_news_data import getNews
from datetime import date,timedelta
import dateutil.parser
import numpy as np
from matplotlib import pyplot as plt
import yfinance as yf
import streamlit as st

# TICKER = 'SPY'
# API_KEY = 'ced42af865c5482aa78652be689b4af0'
# KEYWORD = 'doge'

nltk.download('vader_lexicon') #only run this once
def preprocess(API_KEY,KEYWORD,TICKER):
    yf_ticker = yf.Ticker(TICKER)
    hist = yf_ticker.history(period = '1mo')


    BEGIN_DATE = date.today()- timedelta(30)
    BEGIN = BEGIN_DATE.strftime('%Y-%m-%d')
    END = date.today().strftime('%Y-%m-%d')




    df = getNews(API_KEY,KEYWORD,BEGIN,END)
    df['count'] = 1
    news_df = df[['title','description','url','urlToImage','publishedAt']]
    analyzer  = SentimentIntensityAnalyzer()

    for i in range(len(df)):
        titleSentiment = analyzer.polarity_scores(df['title'][i])['compound']
        descriptionSentiment = analyzer.polarity_scores(df['description'][i])['compound']
        df.loc[i,'sentiment'] = (titleSentiment + descriptionSentiment) / 2
        df.loc[i,'datetime'] = dateutil.parser.parse(df.loc[i,'publishedAt']).strftime('%Y-%m-%d')

    df_daily = df.groupby('datetime').mean().loc[:,['sentiment']]
    df_daily['numNews'] = df.groupby('datetime').sum().loc[:,'count']
    df_daily.index = pd.DatetimeIndex(df_daily.index)
    result_df = pd.concat([hist,df_daily],axis = 1)

    result_df = result_df.loc[df_daily.index[0]:df_daily.index[-1],:]
    result_df['numNews'].fillna(0,inplace = True)
    result_df['sentiment'].fillna(method = 'ffill',inplace = True)
    result_df = result_df[result_df['Close'].notna()]
    return news_df, result_df



def plt_sentiment_and_count(result_df):
    #st.line_chart(data=result_df[['sentiment','numNews']], width=0, height=0, use_container_width=True)
    #
    #Plot graph with 2 y axes
    fig, ax1 = plt.subplots()
    fig.set_size_inches(15,8)
    #Plot bars
    ax1.bar(result_df.index, result_df['numNews'], alpha=0.3)
    ax1.set_xlabel('$Date$')

    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('Number of Articles', color='b')
    [tl.set_color('b') for tl in ax1.get_yticklabels()]
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(color='gray', linestyle='dashed')
    #Set up ax2 to be the second y axis with x shared
    ax2 = ax1.twinx()
    #Plot a line
    ax2.plot(result_df.index, result_df['sentiment'], 'r-')

    # Make the y-axis label and tick labels match the line color.
    ax2.set_ylabel('Sentiment', color='r')
    [tl.set_color('r') for tl in ax2.get_yticklabels()]
    fig.autofmt_xdate()

    #ax1.set_title('Sentiment Analysis - '+ keyword)
    st.pyplot(fig)
    #plt.show()

    # if savefig:
    #     plt.savefig('example_plots/Sentiment Analysis - '+ keyword + '.png')


def plt_sentiment_and_price(result_df):#,keyword,ticker,savefig= False):
    #st.line_chart(data=result_df[['sentiment', 'Close']], width=0, height=0, use_container_width=True)
    #Plot graph with 2 y axes
    fig, ax1 = plt.subplots()
    fig.set_size_inches(15,8)

    #Plot bars
    #ax1.bar(result_df.index, result_df['numNews'], alpha=0.3)
    ax1.plot(result_df.index, result_df['Close'], 'b-')
    ax1.set_xlabel('$Date$')

    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('Price', color='b')
    [tl.set_color('b') for tl in ax1.get_yticklabels()]
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(color='gray', linestyle='dashed')
    #Set up ax2 to be the second y axis with x shared
    ax2 = ax1.twinx()
    #Plot a line
    ax2.plot(result_df.index, result_df['sentiment'], 'r-')

    # Make the y-axis label and tick labels match the line color.
    ax2.set_ylabel('Sentiment', color='r')
    [tl.set_color('r') for tl in ax2.get_yticklabels()]
    fig.autofmt_xdate()
    #ax1.set_title('Sentiment vs Price - '+ keyword + " vs " + ticker)
    st.pyplot(fig)
    # plt.show()
    #
    # if savefig:
    #     plt.savefig('example_plots/Sentiment vs Price - '+ keyword + " vs " + ticker + '.png')
    #
