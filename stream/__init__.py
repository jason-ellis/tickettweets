import json
import datetime
import sys

import tweepy
from .filter import StreamFilter
from config import debug
import re
import os
from flask import Markup
from pymongo import MongoClient

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

users = StreamFilter.users
track = StreamFilter.track
debug_users = StreamFilter.debug_users

# Start MongoDB
conn = MongoClient(os.environ['MONGO_URI'])
db = conn[os.environ['MONGODB_DATABASE']]
collection = db.tweets


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Connected to Twitter")

    def on_data(self, raw_data):
        super(MyStreamListener, self).on_data(raw_data)
        json_data = json.loads(raw_data)
        if 'id_str' in json_data:
            json_data['_id'] = int(json_data['id_str'])
        else:
            print('on_data fired with no id_str')
        # Store tweet in db as JSON
        collection.insert(json_data)

    def on_status(self, status):

        if debug:
            # Assign var for pertinent data from status
            screen_name = status.user.screen_name
            user_name = status.user.name
            user_id = status.user.id_str
            status_id = status.id_str
            status_text = status.text
            tweet_time = status.created_at
            tweet_link = "http://twitter.com/{0}/status/{1}".format(user_id,
                                                                    status_id)

            mentions = [status.entities['user_mentions']['screen_name']
                        for status.entities['user_mentions']
                        in status.entities['user_mentions']]

            print("@{0} mentioned {1} - {2}".format(screen_name,
                                                    mentions,
                                                    tweet_link))
            print("\t{0}".format(status_text))

    def on_error(self, status_code):
        print("Error {0} encountered".format(status_code))
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('Encountered status code 420. Quitting')
            return False

    def on_timeout(self):
        print("Timeout occurred at {}".format(datetime.datetime.now()))
        return

    def on_disconnect(self, notice):
        print("Disconnected at {}".format(datetime.datetime.now()))
        print("Twitter sent the following disconnect message: \n{}"
              .format(notice))
        return


def start_stream():

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()

    # encoding() removed from if follow and if track in Stream.filter for Py3
    myStream = tweepy.Stream(auth=api.auth,
                             listener=myStreamListener,
                             retry_count=5)

    # Lookup users whether given an ID (most accurate) or a screen name
    user_ids = []
    screen_names = []

    for item in users:
        for host in item['hosts']:
            if host['user_id']:
                user_ids.append(host['user_id'])
            elif host['screen_name']:
                screen_names.append(host['screen_name'])
            else:
                # TODO report error
                if debug:
                    print('User {} not found'.format(host))

    if debug:
        screen_names.extend(debug_users)

    user_data = api.lookup_users(screen_names=screen_names, user_ids=user_ids)

    if debug:
        for user in user_data:
            print("Following: {0} - @{1} ({2})".format(user.name,
                                                       user.screen_name,
                                                       user.id_str))

    follow_ids = [user.id_str for user in user_data]
    myStream.filter(follow=follow_ids, async=True)


# TODO user_ids should be submitted to view from form
# Return tweets from database
def get_tweets(limit=0,
               user_ids=users,
               mentions=True,
               cursor=None,
               age='old',
               sort='_id',
               order=-1):
    """
    :param limit: maximum number of tweets to return
    :type limit: int
    :param user_ids: list of user IDs to track
    :type user_ids: list
    :param mentions: whether to include mentions of users in user_ids
    :type mentions: bool
    :param cursor: reference tweet for results, default=None
    :type cursor: int
    :param age: direction from cursor, old or new, default='old'
    :type age: str
    :param sort: sort field, default='_id'
    :type sort: str
    :param order: order of returned tweets, default=-1 (descending)
    :type order: int
    :return: list of tweets returned from query
    :rtype: list
    """

    user_query = []
    # TODO remove this for statement once user_ids are passed from site
    for item in user_ids:
        for host in item['hosts']:
            if host['user_id']:
                user_query.append(host['user_id'])

    tweets = []
    tweet_query = {'text': {'$exists': True}}
    if cursor:
        if age is 'old':
            direction = '$lt'
        elif age is 'new':
            direction = '$gt'
        tweet_query['_id'] = {direction: cursor}
        if debug:
            try:
                cursor_tweet = collection.find_one({'_id': cursor})
                print('Cursor tweet {0} created at {1}'
                      .format(cursor,
                              cursor_tweet['created_at']))
            except TypeError as e:
                print('**Error encountered finding the cursor. {} not found'
                      .format(cursor))
                print('**TypeError: {}'.format(e))
            except:
                e = sys.exc_info()[0]
                print('**Other Error: {}'.format(e))

    if mentions:
        tweet_query['$or'] = [{'user.id_str': {'$in': user_query}},
                              {'in_reply_to_user_id_str': {'$in': user_query}}]
    else:
        tweet_query['user.id_str'] = {'$in': user_query}

    if debug:
        print(tweet_query)

    for tweet in collection.find(tweet_query)\
            .sort(sort, order).limit(limit):
        if 'retweeted_status' in tweet:
            tweet['retweeted_status']['text'] = \
                add_entities(tweet['retweeted_status']['text'],
                             tweet['retweeted_status']['entities'])
        tweet['text'] = add_entities(tweet['text'], tweet['entities'])
        tweets.append(tweet)
    return tweets


# add links to entities in tweet
def add_entities(tweet_text, tweet_entities):
    # Per Twitter API, tolerant of possible empty/null values
    if 'urls' in tweet_entities:
        for url in tweet_entities['urls']:
            tweet_text = re.sub(
                url['url'],
                '<a href="{0}" title="{1}" target="_blank">{2}</a>'
                .format(url['url'],
                        url['expanded_url'],
                        url['display_url']),
                tweet_text, flags=re.IGNORECASE)
    if 'user_mentions' in tweet_entities:
        for user in tweet_entities['user_mentions']:
            tweet_text = re.sub(
                '@{0}'.format(user['screen_name']),
                '<a href="https://twitter.com/intent/follow?screen_name={0}" '
                'target="_blank">@{0}</a>'.format(user['screen_name'],
                                                  user['screen_name']),
                tweet_text, flags=re.IGNORECASE)
    if 'media' in tweet_entities:
        for media in tweet_entities['media']:
            tweet_text = tweet_text.replace(media['url'], '')
    if 'hashtags' in tweet_entities:
        for hashtag in tweet_entities['hashtags']:
            tweet_text = re.sub(
                '#{0}'.format(hashtag['text']),
                '<a href="http://twitter.com/search?q=%23{0}" '
                'target="_blank">#{0}</a>'
                .format(hashtag['text']),
                tweet_text, flags=re.IGNORECASE)
    tweet_text = Markup(tweet_text)
    return tweet_text

if __name__ == '__main__':
    start_stream()