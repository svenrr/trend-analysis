import spacy
from collections import Counter
from string import punctuation
import math
import en_core_web_md
import streamlit as st
import pandas as pd 
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp = en_core_web_md.load()

def word_frequency(article_text):
    from spacy.lang.en.stop_words import STOP_WORDS
    stopwords = list(STOP_WORDS)
    
    doc = nlp(article_text.lower()) 
    
    word_freqs = {}
    for word in doc:
        if (word.text not in stopwords and word.text not in punctuation and word.text not in '“”‘’'):
            if word.text not in word_freqs.keys():
                word_freqs[word.text] = 1
            else:
                word_freqs[word.text] += 1
                
    sort_orders = sorted(word_freqs.items(), key=lambda x: x[1], reverse=True)
    st.write("---"*40)
    st.write("**Words that appear more than three times:**")

    #for i in sort_orders:
    #    if i[1] > 3:
    #        st.write(i[0], i[1])

    # Save the results in a dataframe and plot it
    wf_dic = dict()
    for i in sort_orders: 
        if i[1] > 3:
            wf_dic.update({i[0] : i[1]})
    
    wf_df = pd.DataFrame(wf_dic, index=["Word Frequencies"])
    st.dataframe(wf_df) 
    
    # Create and generate a word cloud image:
    wc_txt = ""
    for k,v in wf_df.items(): 
      tmp = k + " " 
      wc_txt += (tmp*int(v))
        
    wordcloud = WordCloud(background_color='white').generate(wc_txt)

    # Display the generated image:
    pywc = plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(pywc)
