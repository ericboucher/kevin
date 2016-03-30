# Kevin the Scrapper

import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

 
consumer_key = 'u85eB4hxMGEMRcUOVxPMlx9Dx'
consumer_secret = 'VGT8riFXPMWdU9sAXI0HA28KAiC2xGu1BUnsdb5P9vZ6RfAaOi'
access_token = '702643972783673345-QBULSwJjrhMGIPYjjZ26tZmcwPdv6CN'
access_secret = 'hfiEaieGx2jMqG2W9H51lAX7TC8wpQ4JDsVcWnlvVAlqG'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


def process_or_store(tweet):
    print(json.dumps(tweet))


for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    process_or_store(status._json)


class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])

### Link for streaming process: https://gist.github.com/bonzanini/af0463b927433c73784d