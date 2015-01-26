from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

# Start MongoDB
app.config['MONGO_DBNAME'] = 'tickettweets'
mongo = PyMongo(app, config_prefix='MONGO')

# Start the Twitter stream
from app import stream
stream.main()

# import after tickettweets to prevent circular import
from app import views
