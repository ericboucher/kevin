import time
import tweepy
import json
from kevin_twitter_access import initialize_api, create_stream
 
api, auth = initialize_api()

trendsUS = api.trends_place(id = 23424977)
# TO DO - Order By tweet_volume
hashtags = [x['name'] for x in trendsUS[0]['trends'] if x['name'].startswith('#')]
print hashtags
trends_hashtag = hashtags[0:10]

# Create Stream
create_stream(trends_hashtag)