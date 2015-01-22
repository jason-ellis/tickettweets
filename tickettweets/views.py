from tickettweets import tickettweets


@tickettweets.route("/")
@tickettweets.route("/index")
def index():
    return "Hello World!"

if __name__ == "__main__":
    tickettweets.run()