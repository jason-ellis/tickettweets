import os

# global debug settings
debug = True

basedir = os.path.abspath(os.path.dirname(__file__))

# database config


WTF_CSRF_ENABLED = True
# TODO create a secret key
SECRET_KEY = 'you-will-never-guess'