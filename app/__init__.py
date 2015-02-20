from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.moment import Moment

app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)

from stream import start_stream
start_stream()

# import after app to prevent circular import
from app import views

