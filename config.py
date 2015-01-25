import os


basedir = os.path.abspath(os.path.dirname(__file__))

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tickettweets.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
# TODO create a secret key
SECRET_KEY = 'you-will-never-guess'