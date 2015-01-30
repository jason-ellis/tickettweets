from flask import Flask
from pymongo import Connection
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Start MongoDB
conn = Connection()
db = conn.tickettweets
collection = db.tweets

from stream import start_stream
start_stream()

# import after app to prevent circular import
from app import views

