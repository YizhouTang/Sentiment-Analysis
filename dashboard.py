import streamlit as st
import sentiment_analysis as sa

st.title("Sentiment Analysis")
st.write("#### Author: Eric Tang")
st.write("#### Last update: 2021-05-23")
st.write("### Given keyword(s) from user input, this app pulls the latest related articles, assigns a sentiment score for each article based on the title/descriptions, and then generates a timeseries of sentiment scores for analysis purposes.")

#API_KEY = '4182ed52673d404ea2b0a9187f258c0c'
API_KEY = st.text_input("Please enter your API key:", 'ced42af865c5482aa78652be689b4af0')
KEYWORD = st.text_input("Keywords for sentiment analysis:","doge")
TICKER =  st.text_input("Please enter a ticker:","SPY")



news_df, result_df = sa.preprocess(API_KEY,KEYWORD,TICKER)
st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 400px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
for i in range(0,5):
    st.sidebar.title("Related News - " + KEYWORD)
    st.sidebar.image(
        news_df.loc[i,'urlToImage'],
        width=250,  # Manually Adjust the width of the image as per requirement
    )
    st.sidebar.markdown(news_df.loc[i,'title'])
    st.sidebar.markdown(news_df.loc[i, 'url'])

st.write("## Sentiment Analysis - " + KEYWORD)
sa.plt_sentiment_and_count(result_df)


st.write('## Sentiment vs Price - '+ KEYWORD + " vs " + TICKER)
sa.plt_sentiment_and_price(result_df)

