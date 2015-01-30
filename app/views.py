import json
import sys

from app import app, collection
from stream import debug
from flask import render_template, request, Response


@app.route("/")
def index():
    tweets = []
    for tweet in collection.find().sort('_id', -1).limit(20):
        tweets.append(tweet)
    return render_template('index.html',
                           tweets=tweets,
                           debug=debug)

@app.route("/_new_tweets")
def new_tweets():
    cursor = request.args.get('cursor', 0, type=int)
    try:
        cursor_tweet = collection.find_one({'_id': cursor})
        if debug:
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
    updated_tweets = []
    for tweet in collection.find({'_id': {'$gt': cursor}}).sort('_id', -1):
        print('tweet {0} created at {1}'.format(tweet['_id'],
                                                tweet['created_at']))
        updated_tweets.append(tweet)
    updated_tweets = json.dumps(updated_tweets)
    resp = Response(response=updated_tweets,
                    status=200,
                    mimetype="application/json")
    return resp