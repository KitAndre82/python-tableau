#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:44:16 2022

@author: andrew
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#reading excel/xlsx files

data = pd.read_excel('articles.xlsx')

#summary of the data

data.describe()
data.info()

#number of articles per source

data.groupby(['source_id'])['article_id'].count()

#number of reactions per publisher

data.groupby(['source_id'])['engagement_reaction_count'].sum()

data.describe()
data.info()
        
#creating a keyword flag

# length=len(data)
# keyword = 'crash'
# keyword_flag=[]
# for x in range(0,length):
#     if keyword in data['title'][x]:
#         flag=1
#     else:
#         flag=0
#     keyword_flag.append(flag)
    
#creating a function for the above

def keywordflag(keyword):
    length=len(data)
    keyword_flag=[]
    for x in range(0,length):
        heading = data['title'][x]
        try:
            if keyword in heading:
                flag=1
            else:
                flag=0
        except:
            flag=0
        keyword_flag.append(flag)      
    return keyword_flag
        
keywordflag = keywordflag('murder')

#creating a new column

data['keyword_flag'] = pd.Series(keywordflag)

#SentimentIntensityAnalyzer()

sent_int = SentimentIntensityAnalyzer()

text = data['title'][16]

sent = sent_int.polarity_scores(text)

pos = sent['pos']
neg = sent['neg']
neu = sent['neu']

#determining sentiment for a column
title_neg_sentiment=[]
title_pos_sentiment=[]
title_neu_sentiment=[]
length = len(data)

for x in range(0, length):
    try:      
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sentiment = sent_int.polarity_scores(text)
        pos = sentiment['pos']
        neg = sentiment['neg']
        neu = sentiment['neu']
    except:
        neg=0
        pos=0
        neu=0
    title_pos_sentiment.append(pos)
    title_neg_sentiment.append(neg)
    title_neu_sentiment.append(neu)

#creating sentiment columns in our data frame

data['title_positive_sentiment'] = pd.Series(title_pos_sentiment)
data['title_negative_sentiment'] = pd.Series(title_neg_sentiment)
data['title_neutral_sentiment'] = pd.Series(title_neu_sentiment)

#saving the new and cleaned file as an excel file

data.to_excel('blogme_clean.xlsx' , sheet_name='blogme_data', index = False)
