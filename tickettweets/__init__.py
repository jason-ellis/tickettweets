from flask import Flask

tickettweets = Flask(__name__)

# import after tickettweets to prevent circular import
from tickettweets import views