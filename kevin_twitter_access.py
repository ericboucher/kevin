""" This module defines the base functions to interact with the twitter API.""" # Kevin the Scrapper
import time
import json
import tweepy
#import utils
#import datetime
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
#from Filters import Filter, FiltersList

# Authentication
with open("./client_secrets_twitter.json") as data_file:
    CLIENT_SECRETS_TWITTER = json.load(data_file)

CONSUMER_KEY = CLIENT_SECRETS_TWITTER['consumer_key']
CONSUMER_SECRET = CLIENT_SECRETS_TWITTER['consumer_secret']
ACCESS_TOKEN = CLIENT_SECRETS_TWITTER['access_token']
ACCESS_SECRET = CLIENT_SECRETS_TWITTER['access_secret']

AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


def process_tweet(data):
    """process raw tweet"""
    mtweet = json.loads(data)
    # We only want to write tweets; we'll skip 'delete' and
    # 'limit' information.
    if 'delete' in mtweet:
        print "contained delete"
        return True
    if 'limit' in mtweet:
        return True

    dump = {}
    dump['created_at'] = mtweet['created_at']
    dump['text'] = mtweet['text'].encode('ascii', 'ignore')
    return dump

def store_tweet(data):
    """process raw tweet"""
    mtweet = json.loads(data)
    # We only want to write tweets; we'll skip 'delete' and
    # 'limit' information.
    if 'delete' in mtweet:
        print "contained delete"
        return True
    if 'limit' in mtweet:
        return True

    with open('twitter_stream_trending.json', 'a') as destination_file:
        dump = {}
        dump['created_at'] = mtweet['created_at']
        ## TO DO - Change as Timestamp
        ## TO DO - Add trend #hashtag
        dump['text'] = mtweet['text'].encode('ascii', 'ignore')
        #print dump
        destination_file.write(json.dumps(dump))
        destination_file.write("\n")

def initialize_api():
    """Initialize an API
    :return: tweepy api and auth
    """
    return tweepy.API(AUTH), AUTH

def get_timeline_status():
    for status in tweepy.Cursor(API.home_timeline).items(1):
       # Process a single status
       print status._json

class SimpleListener(StreamListener):
    """StreamListener implementation"""
    def __init__(self):
        StreamListener.__init__(self)
        self.count = 0

    def on_data(self, data):
        try:
            process_tweet(data)
            self.count += 1
            if self.count%10 == 0:
                print "%d Tweets Processed"%self.count
            return True
        except BaseException as base_error:
            print "Error on_data: %s" % str(base_error)
            time.sleep(5)

        return True

    def on_error(self, status):
        print status
        return True

class ActiveListener(StreamListener):
    """StreamListener implementation"""
    def __init__(self, new_reqs=[]):
        StreamListener.__init__(self)
        self.count = 0
        self.new_requests = new_reqs

    def on_data(self, data):
        #try:
        dump = process_tweet(data)
        self.count += 1

        # TOdO if tweet contains #kevinthebot
        # Add request to list

        if "#kevinthebot" in dump['text']:
            print dump['text']
            self.new_requests.append(dump)
            print self.new_requests

        if self.count%10 == 0:
            print "%d Tweets Processed"%self.count

        return True

    def get_requests(self):
        return self.new_requests

    def on_error(self, status):
        print status
        return True

# class RegisterTweet(StreamListener):
#     """Another Listener"""
#     # todo - Change this function to register new requests from users, or remove
#     # Option1 - Hey @KevinBot, please follow XXX.
#     # Option2 - Thanks @kevinBot, I'm all set.

#     def on_data(self, data):

#         json_data = json.loads(data.strip())

#         retweeted = json_data.get('retweeted', False)
#         from_self = json_data.get('user', {}).get('id_str', '') == "KEVIN_TWITTER_ID"

#         if retweeted is not None and not retweeted and not from_self:

#             tweet_id = json_data.get('id_str')
#             screen_name = json_data.get('user').get('screen_name')
#             tweet_text = json_data.get('text')

#             print tweet_id, screen_name, tweet_text
#             #chatResponse = chatbot.respond(tweetText)
#             # process stream data here

#             #replyText = '@' + screen_name + ' ' + chatResponse

#         #if len(replyText) > 140:
#         #        replyText = replyText[0:137] + '...'
#         #API.update_status(replyText, tweet_id)

#     def on_error(self, status):
#         print status

HASHTAGS_LIST = [u'#WHCD', u'#5WordLieToYourSpouse', u'#RDMA', u'#VindictiveSongs',
                 u'#IfIMadeAMovie', u'#MikeysNewVideo', u'#independentbookstoreday',
                 u'#stumpthetruck', u'#SparksEnergy300', u'#iHeartCountry']

def get_trends(n_trends=10):
    """ This function allows you to get the n top trends"""
    api, _ = initialize_api()

    trends_us = api.trends_place(id=23424977)
    # TO DO - Order By tweet_volume
    hashtags = [x['name'] for x in trends_us[0]['trends'] if x['name'].startswith('#')]
    trends_hashtag = hashtags[0:n_trends]
    return trends_hashtag

def create_stream(hashtags_list=["#python"]):
    """stream_creator"""
    twitter_stream = Stream(AUTH, SimpleListener())
    twitter_stream.filter(track=hashtags_list, async=True)
    return twitter_stream

def initialize_stream(listener, hashtags_list=["#python"]):
    """stream_creator"""
    _, auth = initialize_api()
    twitter_stream = Stream(auth, listener)
    twitter_stream.filter(track=hashtags_list, async=True)
    return twitter_stream

def self_updating_trendy_stream():  
    trends_list = get_trends()
    twitter_stream = create_stream(trends_list)
    while True:
        new_trends = get_trends()
        if trends_list != new_trends:
            print "Updating List of trends"
            trends_list = new_trends
            twitter_stream.disconnect()
            twitter_stream.filter(track=trends_list, async=True)
        time.sleep(60)

if __name__ == "__main__":
    #filters_list = FiltersList([Filter("#python", 1)])
    self_updating_trendy_stream()