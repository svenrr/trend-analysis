import streamlit 
from news_scraping import get_urls_from_feed

st.write("# BBC News Scraper")

if st.button("Fetch..."): 
  get_urls_from_feed()
