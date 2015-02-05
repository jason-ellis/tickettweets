import tweepy
from .filter import users, track, debug_users
from app.keys import *
from app import collection
from config import debug
import json


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

            if screen_name in users:
                print('--------------')
                print("|--| {0}".format(user_name))
                print("|__| @{0}".format(screen_name))
                print(status_text)
                print('\n')
                print("Reply, Retweet, Favorite")
                print("{0} - {1}".format(tweet_time, tweet_link))
                print(status.source)
                print('--------------')
                return True
            else:
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


def start_stream():

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()

    # encoding() removed from if follow and if track in Stream.filter for Py3
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # Lookup users whether given an ID (most accurate) or a screen name
    user_ids = []
    screen_names = []

    for user in users:
        if user['user_id']:
            user_ids.append(user['user_id'])
        elif user['screen_name']:
            screen_names.append(user['screen_name'])
        else:
            # TODO report error
            if debug:
                print('User {} not found'.format(user))

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

if __name__ == '__main__':
    start_stream()