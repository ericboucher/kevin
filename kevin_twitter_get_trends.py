""" This module allows to fetch the last trends trends"""
from kevin_twitter_access import initialize_api

def get_trends():
    """ This functions allows you to get trends"""
    api, _ = initialize_api()

    trends_us = api.trends_place(id=23424977)
    # TO DO - Order By tweet_volume
    hashtags = [x['name'] for x in trends_us[0]['trends'] if x['name'].startswith('#')]
    print hashtags
    trends_hashtag = hashtags[0:10]
    return trends_hashtag

if __name__ == "__main__":
    get_trends()
