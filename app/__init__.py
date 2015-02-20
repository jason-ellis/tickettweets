from flask import Flask
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from flask.ext.moment import Moment

app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)

# Start MongoDB
conn = MongoClient()
if 'tickettweets-production' in conn.database_names():
    # production DB named by dokku-mongodb-plugin
    db = conn['tickettweets-production']
else:
    # dev database
    db = conn.tickettweets
collection = db.tweets

from stream import start_stream
start_stream()

# import after app to prevent circular import
from app import views

