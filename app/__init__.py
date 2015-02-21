from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.moment import Moment

app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)

# import after app to prevent circular import
from app import views

