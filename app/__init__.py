from flask import Flask

from app import stream

app = Flask(__name__)


# Start the Twitter stream
stream.main()

# import after tickettweets to prevent circular import
from app import views