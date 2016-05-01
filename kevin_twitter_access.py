# Kevin the Scrapper
import time
import tweepy
import json
import utils
import datetime
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Authentication
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

def initialize_api():
    return tweepy.API(auth), auth

#for status in tweepy.Cursor(api.home_timeline).items(1):
#    # Process a single status
#    process_or_store(status._json)

count = 0

class MyListener(StreamListener):
    def on_data(self, data):
        global count
        mtweet = json.loads(data)
        # We only want to write tweets; we'll skip 'delete' and
        # 'limit' information.
        if 'delete' in mtweet:
            print "contained delete"
            return True
        if 'limit' in mtweet:
            return True


        try:
            with open('twitter_stream_trending.json', 'a') as f:
                dump = {}
                dump['created_at'] = mtweet['created_at']
                ## TO DO - Change as Timestamp
                ## TO DO - Add trend #hashtag
                dump['text'] = mtweet['text'].encode('ascii', 'ignore')
                f.write(json.dumps(dump))
                f.write("\n")
                count+=1
                if count%10 == 0:
                    print "%d Tweets Saved"%count
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True
 
    def on_error(self, status):
        print(status)
        return True

class RegisterTweet(StreamListener):

    #TODO - Change this function to register new requests from users, or remove
    # Option1 - Hey @KevinBot, please follow #XXX.
    # Option2 - Thanks @kevinBot, I'm all set.
 
    def on_data(self, data):
 
    jsonData = json.loads(data.strip())
     
    retweeted = tweet.get('retweeted', False)
    from_self = tweet.get('user',{}).get('id_str','') == account_user_id
 
    if retweeted is not None and not retweeted and not from_self:
 
        tweetId = jsonData.get('id_str')
        screenName = jsonData.get('user').get('screen_name')
        tweetText = jsonData.get('text')
 
        chatResponse = chatbot.respond(tweetText)
        # process stream data here

        replyText = '@' + screenName + ' ' + chatResponse
     
    if len(replyText) > 140:
            replyText = replyText[0:137] + '...'
 
    twitterApi.update_status(replyText, tweetId)
 
    def on_error(self, status):
        print status
 

hashtags_list = [u'#WHCD', u'#5WordLieToYourSpouse', u'#RDMA', u'#VindictiveSongs', u'#IfIMadeAMovie', u'#MikeysNewVideo', u'#independentbookstoreday', u'#stumpthetruck', u'#SparksEnergy300', u'#iHeartCountry']

def create_stream(hashtags_list = []):
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=hashtags_list)

### Link for streaming process: https://gist.github.com/bonzanini/af0463b927433c73784d