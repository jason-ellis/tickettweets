from datetime import datetime

from app import app
from stream import debug, users, get_tweets
from flask import render_template, request


@app.route("/")
def index():
    tweets = get_tweets(limit=20)
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
    updated_tweets = get_tweets(cursor=cursor_id, age='new')
    updated_tweets_html = []
    for tweet in updated_tweets:
        tweet_html = render_template('tweet.html',
                                     tweet=tweet,
                                     new='new-tweet',
                                     debug=debug)
        updated_tweets_html.append(tweet_html)
    updated_tweets_html = '\n'.join(updated_tweets_html)
    return updated_tweets_html

# AJAX call for more older tweets
@app.route("/_more_tweets")
def more_tweets():
    last_tweet_id = request.args.get('last_tweet_id', 0, type=int)
    older_tweets = get_tweets(cursor=last_tweet_id, age='old', limit=20)
    older_tweets_html = []
    for tweet in older_tweets:
        tweet_html = render_template('tweet.html',
                                     tweet=tweet,
                                     debug=debug)
        older_tweets_html.append(tweet_html)
    older_tweets_html = '\n'.join(older_tweets_html)
    return older_tweets_html

# Parse datetime of tweets
@app.template_filter('parse_date')
def parse_date(tweet_date):
    parsed_date = datetime.strptime(tweet_date, '%a %b %d %H:%M:%S %z %Y')
    return parsed_date