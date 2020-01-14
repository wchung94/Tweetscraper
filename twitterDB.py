# Import statements

import pandas as pd
import numpy as np
import re
import datetime as dt
import GetOldTweets3 as got


def read_tweet_queries(hashtag_path):
    
    with open(hashtag_path) as hp:
        lines = hp.readlines()
        lines = ['#' + line.strip() for line in lines]

    return(lines)

def tweet_scrape(text_query, start_date = None, end_date = None, count = 100):
    # Scrape most recent tweets containing the tags.
    
    today = dt.datetime.today().strftime('%Y-%m-%d') 
    tomorrow = (dt.datetime.today() + dt.timedelta(days=1)).strftime('%Y-%m-%d') 
    
    
    if start_date == None:
        start_date = today
    if end_date == None:
        end_date = tomorrow

    
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(text_query)\
                                           .setSince(start_date)\
                                           .setUntil(end_date)\
                                           .setMaxTweets(count)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # Creating list of chosen tweet data
    tweet_df = pd.DataFrame()
    tweet_df['Datetime'] = [tweet.date for tweet in tweets]
    tweet_df['Username'] = [tweet.username for tweet in tweets]
    tweet_df['Tweet'] = [tweet.text for tweet in tweets]
    tweet_df['Retweets'] = [tweet.retweets for tweet in tweets]
    tweet_df['Favorites'] = [tweet.favorites for tweet in tweets]
    tweet_df['Mentions'] = [tweet.mentions for tweet in tweets]
    tweet_df['Hashtags'] = [tweet.hashtags for tweet in tweets]
    tweet_df['Geo'] = [tweet.geo for tweet in tweets]
    return tweet_df

def main():
    
    # read tweet queries to track
    hashtag_path = '/Users/youngmavericks/Documents/TwitterDB/hashtags.txt'
    hashtags = read_tweet_queries(hashtag_path)
    
    # scrape tweet queries of today
    final_tag_df = None
    for tag in hashtags:
        tag_df = tweet_scrape(tag, count=0)
        if (final_tag_df is None) :
            final_tag_df = tag_df
        else:
            final_tag_df = final_tag_df.append(tag_df)

    # store tweet data in Database
    final_tag_json = final_tag_df.to_json(orient='table')
    
    
    return final_tag_json