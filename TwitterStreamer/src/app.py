import json
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch
from datetime import datetime


# import twitter keys and tokens
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
secret_es = os.environ['SECRET_ES']

#create instance of elasticsearch for local docker stack

#es = Elasticsearch([{'host': 'localhost', 'port': 9200}] )

#create instance of elasticsearch for kubernetes cluster
# es = Elasticsearch([
#     'https://elastic:'+secret_es+'@quickstart-es-http:9200'
# ], verify_certs=False )


class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)

        # pass tweet into TextBlob
        tweet = TextBlob(dict_data["text"])

        # output sentiment polarity
        print(tweet.sentiment.polarity)

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # output sentiment
        print(sentiment)

        #fix date format since elasticsearch doesn't automatically recognise twitter dtime format
        dtime = dict_data["created_at"]
        new_datetime = datetime.strftime(datetime.strptime(dtime, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%dT%H:%M:%SZ')

        # add text and sentiment info to elasticsearch
        es.index(index="sentiment",
                 doc_type="_doc",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": new_datetime,
                       "message": dict_data["text"], #todo: need to update type mapping for this to include tag for "field data" so it can be used in tag cloud viz
                       "polarity": tweet.sentiment.polarity,
                       "subjectivity": tweet.sentiment.subjectivity,
                       "sentiment": sentiment})
        return True

    # on failure
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    print("Initializing...")
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    print("Start streaming...")
    # search twitter for "congress" keyword
    stream.filter(track=['tesla', 'elon musk', 'tsla', 'tesla stock', 'tesla model', 'tesla price', 'cybertruck', 'gigafactory'])
