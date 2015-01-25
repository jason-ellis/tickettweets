from tickettweets import db


# TODO refactor for MongoDB
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(140))
    datetime = db.Column(db.DateTime)
    permalink = db.Column(db.VARCHAR)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.string(20))
    name = db.Column(db.string(50))