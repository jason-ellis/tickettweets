import tweepy
from app.keys import *
from app import collection
from config import debug
import json

users = [
    # The Musers
    'GeorgeDunham',
    'junior_miller',
    'gordonkeith',
    # Norm Hitzges
    'NormsClubhouse',
    # BaD Radio
    'SportsSturm',
    'bracketdan',
    'GreatDonovan',
    'NotJackKemp',
    # The Hardline
    'theoldgreywolf',
    'corbydavidson',
    'badkaratemovie',
    # Cirque du Sirois
    'MikeSirois',
    'CashSports',
    # Ticker guys and JV
    'sbass1310',
    'tlw716',
    'killer1310',
    'CincoDeMino',
    'CreyTrey1310',
    'poponjer',
    'JustinMonty',
    'FAHY1015',
    'machinesports',
    'TC1310'
]

if debug is True:
    print("___Debug mode___")
    users.extend(['JasonDFW', 'SoccerlessSturm', 'SportsSlurm'])

track = None


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Connected to Twitter")

    def on_data(self, raw_data):
        super(MyStreamListener, self).on_data(raw_data)
        # Store tweet in db
        collection.insert(json.loads(raw_data))

    def on_status(self, status):

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
            # print(status)
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

    user_data = api.lookup_users(screen_names=users)
    for user in user_data:
        print("Following: {0} - @{1} ({2})".format(user.name,
                                                   user.screen_name,
                                                   user.id_str))
    user_ids = [user.id_str for user in user_data]
    # print(api.rate_limit_status())
    myStream.filter(follow=user_ids, async=True)

if __name__ == '__main__':
    start_stream()