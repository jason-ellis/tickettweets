import json
import sys

from app import app, collection
from stream import debug
from flask import render_template, request, Response


@app.route("/")
def index():
    tweets = []
    for tweet in collection.find({ 'text': {'$exists': True}})\
            .sort('_id', -1).limit(20):
        tweets.append(tweet)
    if debug:
        print('Sent {0} tweets to DOM'.format(len(tweets)))
    return render_template('index.html',
                           tweets=tweets,
                           debug=debug)


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
        print('tweet {0} created at {1}'.format(tweet['_id'],
                                                tweet['created_at']))
        tweet_html = render_template('tweet.html',
                        tweet=tweet,
                        debug=debug)
        updated_tweets.append(tweet_html)
    updated_tweets = ' '.join(updated_tweets)
    return updated_tweets

# AJAX call for new tweets
"""@app.route("/_new_tweets")
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
        print('tweet {0} created at {1}'.format(tweet['_id'],
                                                tweet['created_at']))
        updated_tweets.append(tweet)
    updated_tweets = json.dumps(updated_tweets)
    resp = Response(response=updated_tweets,
                    status=200,
                    mimetype="application/json")
    return resp"""

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
        older_tweets.append(tweet)
    older_tweets = json.dumps(older_tweets)
    resp = Response(response=older_tweets,
                    status=200,
                    mimetype="application/json")
    return resp