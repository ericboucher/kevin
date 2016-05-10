""" A stream that refreshes every minute or so to take into account incoming requests"""
import time, signal, sys
from kevin_twitter_access import ActiveListener, get_trends, initialize_stream
from Filters import Filter, FiltersList

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    TWITTER_STREAM.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# To Do - turn into a class?

if __name__ == "__main__":
    print "Starting Listener and Stream"
    REFRESH_RATE = 60
    LISTENER = ActiveListener()
    TRENDS_LIST = get_trends(2)
    TWITTER_STREAM = initialize_stream(LISTENER, TRENDS_LIST)
    filters = FiltersList #filters we are following
    while True:
        new_requests = LISTENER.get_requests()
        ## To do, add new request to filters
        ## update filters
        ## replace tracking list by filters_list
        if len(new_requests) > 0:
            print "Updating request"
            print new_requests
            TWITTER_STREAM.disconnect()
            TWITTER_STREAM.filter(track=TRENDS_LIST, async=True)
            time.sleep(REFRESH_RATE)