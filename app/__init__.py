from flask import Flask
from pymongo import Connection

app = Flask(__name__)

# Start MongoDB
conn = Connection()
db = conn.tickettweets
collection = db.tweets

# import after app to prevent circular import
from app import views

# Start the Twitter stream
from app import stream
stream.main()
