from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

tickettweets = Flask(__name__)
db = SQLAlchemy(tickettweets)

# import after tickettweets to prevent circular import
from tickettweets import views