from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from tickettweets import stream

tickettweets = Flask(__name__)
db = SQLAlchemy(tickettweets)

# Start the Twitter stream
stream.main()

# import after tickettweets to prevent circular import
from tickettweets import views