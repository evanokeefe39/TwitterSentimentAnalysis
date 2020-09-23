import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime




#todo: set up index with correct types before running script

#make sure es01 is available and connect
retry_strategy = Retry(
    total=10,
    status_forcelist=[413, 429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"],
    backoff_factor=1.5
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

print("connecting...")

res = http.get('http://es01:9200')
print("connection to es01 success!")
print(res.content)

# import twitter keys and tokens
consumer_key = 'GAuhgCwp66h47GODiGzjIQ12T'
consumer_secret = 'FHlGxH7lItMuXHjPy8iITGRbDSBEbKBfFfVl4bHA8GhCYFgNLU'
access_token = '837530140900917248-9kxxjywK8ZocEGAImeabHINI06nH8Xf'
access_token_secret = 'mD2KC3NIYR7Sv6ntTIAuuUrM0cbgtHPFbUnfGR4UNIVln'

#create instance of elasticsearch

es = Elasticsearch([{'host': 'es01', 'port': 9200}] )

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
    print("main...")
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    stream.filter(track=['tesla', 'elon musk', 'tsla', 'tesla stock', 'tesla model', 'tesla price', 'cybertruck', 'gigafactory'])
