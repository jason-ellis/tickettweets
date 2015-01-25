import tweepy
from tickettweets.keys import *
from config import basedir

cache_dir = basedir + '/tweetcache/'

debug = True
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
if debug:
    users.extend(['JasonDFW', 'SoccerlessSturm', 'SportsSlurm'])
track = ['ticket', 'sports']


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Connected to Twitter")

    def on_status(self, status):
        screen_name = status.user.screen_name
        user_name = status.user.name
        user_id = status.user.id_str
        status_id = status.id_str
        status_text = status.text
        tweet_time = status.created_at
        tweet_link = "http://twitter.com/{}/status/{}".format(user_id,
                                                              status_id)

        mentions = [status.entities['user_mentions']['screen_name']
                    for status.entities['user_mentions']
                    in status.entities['user_mentions']]
        if screen_name in users:
            print('--------------')
            print("|--| {}".format(user_name))
            print("|__| @{}".format(screen_name))
            print(status_text)
            print('\n')
            print("Reply, Retweet, Favorite")
            print("{} - {}".format(tweet_time, tweet_link))
            print(status.source)
            print('--------------')
            # print(status)
            with open('{}{}.json'.format(cache_dir, status.id_str),
                      mode='w+',
                      encoding='utf-8') as f:
                f.write(str(status))
            return True
        else:
            print("{} mentioned {} - {}".format(screen_name,
                                                mentions,
                                                tweet_link))

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('Encountered status code 420. Quitting')
            return False


def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    user_data = api.lookup_users(screen_names=users)
    user_ids = []
    for user in user_data:
        print("Following: {} - {} - {}".format(user.name,
                                               user.screen_name,
                                               user.id_str))
    user_ids = [user.id_str for user in user_data]
    # print(api.rate_limit_status())
    myStream.filter(follow=user_ids)

if __name__ == '__main__':
    main()