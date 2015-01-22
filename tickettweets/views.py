from tickettweets import tickettweets
from flask import render_template

@tickettweets.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    tickettweets.run()