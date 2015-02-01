#Ticket Tweets

A live stream of tweets related to The Ticket radio station in Dallas, Texas.

## Currently in development...

This project uses:

Backend: Python, Flask, Jinja2, MongoDB, PyMongo, and Tweepy. 

Frontend: JavaScript and jQuery

The goal of this project is to provide one stop (tickettweets.com when deployed) for Ticket P1s to see all of the Ticket chatter.

The app uses the Twitter streaming API to track all Ticket personalities. It then parses the tweets and feeds them to the user.

Currently, the app displays tweets reverse chronological order, just like Twitter's timeline. It has a refresh button that uses AJAX to load new tweets.

Upcoming enhancements to current state:
- Filter by user or by radio show
- Include or exclude mentions
- Inline or lightbox media
- Auto update stream by default with option for manual refresh

Long-term enhancements:
- Scoreboard/stats included for a better interactive experience during live sporting events
- Twitter oauth to save user preferences
- Trending links among Ticket folks