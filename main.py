import streamlit as st
import pandas as pd 
from pytrends.request import TrendReq
import time
import datetime
import spacy
import altair as alt
from word_frequency import word_frequency
import praw
import tweepy


st.write("# Trend topics & content ideas")
st.write("In the following, different sources are used to quickly gain an overview of current topics in the world or a specific industry. These insights can also be used by journalists, bloggers, etc. to report on topics that are currently of particular interest and most talked about.")

st.markdown("**ToDo:**")
st.markdown("* Analyze comments with VaderScore")
st.markdown("* Just show englisch posts & comments")
st.markdown("* Show news subbreddits with information like subs, hot keywords & trending topcis --> view documentation")
st.markdown("* Use google trends")
st.markdown("* Enable search with specific keywords")
#######################################################################################################################################################


#######################################################################################################################################################
st.write("----")
st.write("# Reddit Live Test")

r = praw.Reddit(client_id='ddxZYbBilApY5A', client_secret='4rxjgOizdOJlhuyD781bi4tCqH8', user_agent='Henlo')

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
    for submission in r.subreddit(subr).hot(limit=10):
        topic_lst.append(submission.title)

st.write(topic_lst)

st.write("Top 10 keywords:")
word_frequency(". ".join(topic_lst))

#######################################################################################################################################################

st.write("----")
st.write("# Google related queries")

pytrend = TrendReq()
search_topic = st.text_input("Enter a keyword or topic...","Data Science",key="gtrend") 

sb_torr = st.selectbox("Select one option", ["top", "rising"], key="sb_torr")

def gtrends(keyword, torr): #top or rising?
    pytrend.build_payload(kw_list=[keyword])
    related_queries = pytrend.related_queries()
    rq = pd.DataFrame(related_queries.get(keyword).get(torr))
    return rq

rq_data = gtrends(search_topic, sb_torr)
st.dataframe(rq_data)
#######

st.markdown("**Interest over time (US)**")
rd_tf = st.radio("Select google property (default = web searches", ["","news", "youtube"])
sb_tf = st.selectbox("Select a timeframe", ["today 5-y", "today 3-y", "today 12-m", "today 3-m", "today 1-m"] , key="sb_tf")
iot_kws = st.text_input("Enter keywords and use comma as delimiter","python, java, html, javascript, sql", key="giot")
keywords = list(iot_kws.split(","))
#keywords = ['python', 'java', 'html', 'javascript', 'sql']
interest_over_time = pytrend.build_payload(keywords, timeframe=sb_tf, geo="US", gprop=rd_tf)
iot = pd.DataFrame(pytrend.interest_over_time())
iot.drop("isPartial",axis=1, inplace=True)

st.dataframe(iot)

st.line_chart(iot)


#########

st.markdown("**Interest by region**")
ibr = pytrend.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
st.dataframe(ibr)

##########

st.markdown("**Trending Searches (Real Time)**")
country = st.text_input("Enter a country","united_states")
ts = pd.DataFrame(pytrend.trending_searches(pn=country))
st.dataframe(ts)

##########

st.markdown("**Related Topics**")
rt = pd.DataFrame(pytrend.related_topics().get("Data Science"))
st.dataframe(rt)

##########

st.markdown("**Top Charts (Global)**")
rt_date = st.textinput("Enter a date (YYYYMM or YYYY)","202010")
rt = pd.DataFrame(pytrend.top_charts(rt_date, hl='en-US', tz=300, geo='GLOBAL')) #or tz=360?
rt.drop("exploreQuery",axis=1, inplace=True)
st.dataframe(rt)

##########

st.markdown("**Suggestions**")
sugg = pd.DataFrame(pytrend.suggestions(search_topic))
st.dataframe(sugg)


#######################################################################################################################################################

st.markdown("# Top10 Twitter Trending Topics (USA)")
twitter_trends = pd.read_csv("https://docs.google.com/spreadsheets/d/1ZQmt6uL-MYrb8UacoOhRGaBTUzlelPOz6eti5kqeWWc/export?gid=0&format=csv")
twitter_trends = twitter_trends.tail(10).reset_index(drop=True)
st.write("Last update: {}".format(twitter_trends["date_time"][0]))
st.dataframe(twitter_trends[["trends", "tweet_volume"]])      

tt_plot = alt.Chart(twitter_trends).mark_bar().encode(x="tweet_volume:Q", y="trends:O").properties(width=600, height=400) #sort="tweet_volume:Q"
st.altair_chart(tt_plot)

#################


#st.write("----")
#st.write("# Twitter Live Test")

## Twitter Developer keys here
#consumer_key = 'xxx'
#consumer_key_secret = 'yyy'
#access_token = 'zzz'
#access_token_secret = 'qqq'
#
#auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth, wait_on_rate_limit=True)
#
#query = st.text_input("Enter a keyword...", "Data Science", key="twitter")
#
##query = "Trump"
#max_tweets = 50
#searched_tweets = [status for status in tweepy.Cursor(api.search, q=query,tweet_mode='extended').items(max_tweets)]
#search_dict = {"text": [], "author": [], "created_date": []}
#for item in searched_tweets:
#    if not item.retweet or "RT" not in item.full_text:
#        search_dict["text"].append(item.full_text)
#        search_dict["author"].append(item.author.name)
#        search_dict["created_date"].append(item.created_at)
#df_t = pd.DataFrame.from_dict(search_dict)
#st.dataframe(df_t)
#
