import sys
from datetime import datetime

import re
from app import app, collection
from stream import debug, users
from flask import render_template, request, Markup


@app.route("/")
def index():
    tweets = []
    for tweet in collection.find({ 'text': {'$exists': True}})\
            .sort('_id', -1).limit(20):
        if 'retweeted_status' in tweet:
            tweet['retweeted_status']['text'] = \
                add_entities(tweet['retweeted_status']['text'],
                             tweet['retweeted_status']['entities'])
        tweet['text'] = add_entities(tweet['text'], tweet['entities'])
        tweets.append(tweet)
    if debug:
        print('Sent {0} tweets to DOM'.format(len(tweets)))
    return render_template('index.html',
                           tweets=tweets,
                           users=users,
                           debug=debug)

# AJAX call for new tweets
@app.route("/_new_tweets")
def new_tweets():
    cursor_id = request.args.get('cursor', 0, type=int)
    if debug:
        try:
            cursor_tweet = collection.find_one({'_id': cursor_id})
            print('Cursor tweet {0} created at {1}'
                  .format(cursor_id,
                          cursor_tweet['created_at']))
        except TypeError as e:
            print('**Error encountered finding the cursor. {} not found'
                  .format(cursor_id))
            print('**TypeError: {}'.format(e))
        except:
            e = sys.exc_info()[0]
            print('**Other Error: {}'.format(e))
    updated_tweets = []
    for tweet in collection.find({'_id': {'$gt': cursor_id}}).sort('_id', -1):
        if debug:
            print('tweet {0} created at {1}'.format(tweet['_id'],
                                                    tweet['created_at']))
        if 'retweeted_status' in tweet:
            tweet['retweeted_status']['text'] = \
                add_entities(tweet['retweeted_status']['text'],
                             tweet['retweeted_status']['entities'])
        tweet['text'] = add_entities(tweet['text'], tweet['entities'])
        tweet_html = render_template('tweet.html',
                        tweet=tweet,
                        debug=debug)
        updated_tweets.append(tweet_html)
    updated_tweets = '\n'.join(updated_tweets)
    return updated_tweets

# AJAX call for more older tweets
@app.route("/_more_tweets")
def more_tweets():
    last_tweet_id = request.args.get('last_tweet_id', 0, type=int)
    if debug:
        try:
            last_tweet = collection.find_one({'_id': last_tweet_id})
            print('Last tweet {0} created at {1}'
                  .format(last_tweet_id,
                          last_tweet['created_at']))
        except TypeError as e:
            print('**Error encountered finding the cursor. {} not found'
                  .format(last_tweet_id))
            print('**TypeError: {}'.format(e))
        except:
            e = sys.exc_info()[0]
            print('**Other Error: {}'.format(e))
    older_tweets = []
    for tweet in collection.find({'_id': {'$lt': last_tweet_id}})\
            .sort('_id', -1).limit(20):
        print('tweet {0} created at {1}'.format(tweet['_id'],
                                                tweet['created_at']))
        if 'retweeted_status' in tweet:
            tweet['retweeted_status']['text'] = \
                add_entities(tweet['retweeted_status']['text'],
                             tweet['retweeted_status']['entities'])
        tweet['text'] = add_entities(tweet['text'], tweet['entities'])
        tweet_html = render_template('tweet.html',
                        tweet=tweet,
                        debug=debug)
        older_tweets.append(tweet_html)
    older_tweets = '\n'.join(older_tweets)
    return older_tweets

# Parse datetime of tweets
@app.template_filter('parse_date')
def parse_date(tweet_date):
    parsed_date = datetime.strptime(tweet_date, '%a %b %d %H:%M:%S %z %Y')
    return parsed_date


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