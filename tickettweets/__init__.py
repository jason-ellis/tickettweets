from flask import Flask

from tickettweets import stream

tickettweets = Flask(__name__)
db =

# Start the Twitter stream
stream.main()

# import after tickettweets to prevent circular import
from tickettweets import views