import streamlit as st
import pandas as pd 
from pytrends.request import TrendReq
import time
import datetime

import praw
import tweepy

#from news_scraping import get_urls_from_feed
#
#st.write("# BBC News Scraper")
#
#if st.button("Fetch..."): 
#  get_urls_from_feed()


st.write("# Trend topics & content ideas")
st.write("In the following, different sources are used to quickly gain an overview of current topics in the world or a specific industry. These insights can also be used by journalists, bloggers, etc. to report on topics that are currently of particular interest and most talked about.")

st.markdown("**ToDo:**")
st.markdown("* Analyze comments with VaderScore")
st.markdown("* Just show englisch posts & comments")
st.markdown("* Show news subbreddits with information like subs & trending topcis")
st.markdown("* Use google trends")
#######################################################################################################################################################
st.write("----")

st.write("# Live Update Test")

df = pd.read_csv("https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv")
st.dataframe(df)
#######################################################################################################################################################
st.write("----")
st.write("# Reddit Live Test")

reddit_name = "WorldNews"

r = praw.Reddit(client_id='ddxZYbBilApY5A', client_secret='4rxjgOizdOJlhuyD781bi4tCqH8', user_agent='Henlo')
stats = r.subreddit(reddit_name).subscribers
st.write(stats)

###########
st.markdown("**Relevant subreddits for any kind of news**")
srds = pd.read_csv("https://github.com/svenrr/good_news_everyone/raw/main/Datasets/dataset_subreddits_for_eda/subreddits.csv",encoding="cp1252")
st.dataframe(srds)

########
st.write("We take the top 5 subreddits with the most subscribers and search for the top 5 hot topics in there")
srds_top5 = srds.sort_values(by=" subs",ascending=False)[0:5]
st.dataframe(srds_top5)

subr_lst = [i for i in srds_top5.reddit]
topic_lst = []

for subr in subr_lst:
    for submission in reddit.subreddit(subr).hot(limit=10):
        topic_lst.append(submission.title)

st.write(len(topic_lst))
st.write(topic_lst)

#######################################################################################################################################################
st.write("----")
st.write("# Google related queries")

pytrend = TrendReq()
search_topic = st.text_input("Enter a keyword or topic...","Data Science",key="gtrend") 

def gtrends(keyword):
    pytrend.build_payload(kw_list=[keyword])
    related_queries = pytrend.related_queries()
    rq = pd.DataFrame(related_queries.get(keyword).get('rising'))
    return rq

rq_data = gtrends(search_topic)
st.dataframe(rq_data)
#######

st.markdown("**Interest over time**")
keywords = ["Joe Biden", "Donald Trump"]
interest_over_time = pytrend.build_payload(keywords, timeframe="today 5-y", geo="US")
iot = pd.DataFrame(pytrend.interest_over_time())
iot.drop("isPartial",axis=1, inplace=True)

st.dataframe(iot)

st.line_chart(iot)
##########

st.markdown("**Trending Searches in Germany (Real Time)**")
ts = pd.DataFrame(pytrend.trending_searches(pn='germany'))
st.dataframe(ts)

#######################################################################################################################################################
st.write("----")
st.write("# Twitter Live Test")

# Twitter Developer keys here
consumer_key = 'NkzGJC5iKyk2FWjDeSAaEBZZa'
consumer_key_secret = 'BSGX4FEwdreJO1CkoTuKZRH59B56rCK5bt6lTjt0d8DMA4k2D9'
access_token = '1319633638552752128-VpoEssg71W9hFZa2gxDNNdHeMLMmdG'
access_token_secret = 'oEfIJ6Le2DFU0pKmrCDvuLfqznPRTMl5qI3RjA7WL075R'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

query = st.text_input("Enter a keyword...", "Data Science", key="twitter")

#query = "Trump"
max_tweets = 50
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query,tweet_mode='extended').items(max_tweets)]
search_dict = {"text": [], "author": [], "created_date": []}
for item in searched_tweets:
    if not item.retweet or "RT" not in item.full_text:
        search_dict["text"].append(item.full_text)
        search_dict["author"].append(item.author.name)
        search_dict["created_date"].append(item.created_at)
df_t = pd.DataFrame.from_dict(search_dict)
st.dataframe(df_t)
