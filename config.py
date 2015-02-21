import os

# global debug settings
debug = True

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['CSRF_SECRET_KEY']