# Kevin the Scrapper

import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Authorisation
with open("./client_secrets_twitter.json") as data_file:    
    client_secrets_twitter = json.load(data_file)

consumer_key = client_secrets_twitter['consumer_key']
consumer_secret = client_secrets_twitter['consumer_secret']
access_token = client_secrets_twitter['access_token']
access_secret = client_secrets_twitter['access_secret']
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

## Test Auth
def process_or_store(tweet):
    print(json.dumps(tweet))


#for status in tweepy.Cursor(api.home_timeline).items(1):
#    # Process a single status
#    process_or_store(status._json)
count = 0
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python_stream.json', 'a') as f:
                f.write(data)
                count+=1
                print "%d Tweets Saved"%count
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])

### Link for streaming process: https://gist.github.com/bonzanini/af0463b927433c73784d