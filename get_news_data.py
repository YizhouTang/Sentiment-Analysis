from newsapi import NewsApiClient #https://newsapi.org/docs/client-libraries/python
import pandas as pd
import math

def getNews(api_key,keyword,begin_date,end_date):

    SOURCES = 'the-wall-street-journal,' \
               'bloomberg,' \
              # 'business-insider,' \
              # 'fortune'

    DOMAINS = 'wsj.com,' \
              'bloomberg.com,' \
              # 'businessinsider.com,' \
              # 'fortune.com'

    newsapi = NewsApiClient(api_key=api_key)

    all_articles = newsapi.get_everything(q=keyword,
                                          sources= SOURCES,
                                          domains= DOMAINS,
                                          from_param=begin_date,
                                          to=end_date,
                                          language='en',
                                          sort_by='publishedAt',
                                          page=1)
    articles = all_articles['articles']
    numPages = math.ceil(all_articles['totalResults'] / 20)

    if numPages > 1:
           for i in range(2,min(5+1,numPages+1)):#currently only support 5 pages due to free account
                  temp_articles = newsapi.get_everything(q=keyword,
                                                 sources=SOURCES,
                                                 domains=DOMAINS,
                                                 from_param=begin_date,
                                                 to=end_date,
                                                 language='en',
                                                 sort_by='publishedAt',
                                                 page=i)
                  articles.extend(temp_articles['articles'])
    df = pd.DataFrame(articles)
    return df