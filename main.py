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
pd.set_option('display.max_colwidth', -1)

st.write("# Trend topics & content ideas")
st.write("In the following, different sources are used to quickly gain an overview of current topics in the world or a specific industry. These insights can also be used by journalists, bloggers, etc. to report on topics that are currently of particular interest and most talked about.")

st.markdown("**ToDo:**")
st.markdown("* Analyze comments with VaderScore")
st.markdown("* Show news subbreddits with information like subs, hot keywords & trending topcis --> view documentation")

#######################################################################################################################################################

#######################################################################################################################################################
st.write("----")
st.write("# Reddit Live Test")

r_details = pd.read_csv("https://docs.google.com/spreadsheets/d/1WO4GedbP8xiNuLhZc20k51DrCNAmKpL4Uit15pNEqe0/export?gid=0&format=csv")

r = praw.Reddit(client_id=r_details.client_id[0], client_secret=r_details.client_secret[0], user_agent='Henlo')

###########

st.markdown("**Relevant subreddits for any kind of news**")
srds = pd.read_csv("https://github.com/svenrr/good_news_everyone/raw/main/Datasets/dataset_subreddits_for_eda/subreddits.csv",encoding="cp1252")
st.dataframe(srds)

########

st.write("We take the top 10 subreddits with the most subscribers and search for the top 10 hot topics in there. You can change that if you want.")

srds_top10 = srds.sort_values(by=" subs",ascending=False)[0:10]
st.dataframe(srds_top10)

r_ms = st.multiselect("Select subreddits", [i for i in srds.reddit], default=[i for i in srds_top10.reddit])

#subr_lst = [i for i in srds_top5.reddit]
subr_lst = r_ms 
topic_lst = []
reddit_dict = {"subreddit": [], "title": [], "upvote_ratio": [], "num_comments": []}

for subr in subr_lst:
    for submission in r.subreddit(subr).hot(limit=10):
        topic_lst.append(submission.title)
        reddit_dict["subreddit"].append(subr)
        reddit_dict["title"].append(submission.title)
        reddit_dict["upvote_ratio"].append(submission.upvote_ratio)
        reddit_dict["num_comments"].append(submission.num_comments)
       #reddit_dict["score"].append(submission.score)

st.write("Number of total submissions: {}".format(len(topic_lst)))
if st.checkbox("Show full text"):
    st.write(topic_lst)

reddit_df = pd.DataFrame(reddit_dict)
st.dataframe(reddit_df)#.drop(columns="title", axis=0))

st.write("Number of comments: ", reddit_df[reddit_df["subreddit"] == "WorldNews"].num_comments.sum(axis=0))
    
#st.write("Top 10 keywords:")
word_frequency(". ".join(topic_lst))

#######################################################################################################################################################

st.markdown("### Search posts about a specific keyword")
r_search_input = st.text_input("Enter a keyword", "bitcoin")
r_search_sort = st.multiselect("Select sorting option", ["relevance", "hot", "top", "new", "comments"])
r_search_time = st.multiselect("Select time filter option", ["all", "day", "month", "week", "year"] 
#r_search_output = st.slider("How many results should be displayed?", min_value=5, max_value=100, value=10, step=5)

#reddit_search_dict = {"subreddit": [], "title": [], "upvote_ratio": [], "num_comments": []}

search_lst = []
for submission in r.subreddit("all").search(r_search_input, sort=r_search_sort, time_filter=r_search_time):
    search_lst.append(submission.title)
    #add upvote_ratio or score
    #add id/url to find post

st.write(search_lst[0:10])#int(r_search_output)])

#######################################################################################################################################################

st.write("----")
st.write("## Google related queries")

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

st.markdown("## Interest over time (US)")
rd_tf = st.radio("Select google property (default = web searches", ["","news", "youtube"])
sb_tf = st.selectbox("Select a timeframe", ["today 5-y", "today 3-y", "today 12-m", "today 3-m", "today 1-m"] , key="sb_tf")
iot_kws = st.text_input("Enter keywords and use comma as delimiter","python, java, html, javascript, sql", key="giot")
keywords = list(iot_kws.split(","))
interest_over_time = pytrend.build_payload(keywords, timeframe=sb_tf, geo="US", gprop=rd_tf)
iot = pd.DataFrame(pytrend.interest_over_time())
iot.drop("isPartial",axis=1, inplace=True)

st.dataframe(iot)

st.line_chart(iot)


#########

st.markdown("## Interest by region")
ibr = pytrend.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
st.dataframe(ibr)

##########

st.markdown("## Trending Searches (Real Time)")
country = st.text_input("Enter a country","united_states", key="country")
ts = pd.DataFrame(pytrend.trending_searches(pn=country))
st.dataframe(ts)

##########

st.markdown("## Top Charts (Global)")
rt_date = st.slider('Select a date', min_value=2010, max_value=2019, value=2019, step=1)
rt_geo = st.selectbox("Choose a location", ["GLOBAL", "US", "DE"], key="rt_geo")
rt = pd.DataFrame(pytrend.top_charts(rt_date, hl='en-US', tz=300, geo=rt_geo)) #or tz=360?
rt.drop("exploreQuery",axis=1, inplace=True)
st.dataframe(rt)

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
