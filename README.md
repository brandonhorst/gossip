gossip.py
=========

Gossip Chain implementation written in Python 3.x. Will likely not work properly in Python 2.x.

##Running the Program

	python3 run-coding-test.py

##Unit Tests

	python3 test.py

##CLI

	python3 gossip.py Zoe Connor

##Deployment Plan


Heroku is an excellent service that makes deployment very simple. I would define a Procfile that specifies how for Heroku to start my app server, which would be a small Django script functioning as a wrapper around `gossip.py`. Heroku handles the web serving, SSL, load-balancing and such automatically.

I would set up a MongoLab Heroku plugin to run MongoDB and easily store the simple data JSON data in `gossip-chain.json`. I would pull the data using the default Python Mongo driver, and cache it in memory for easy access for future requests.

I would use git to push the source into the Heroku cloud, and Heroku would handle the difficult parts. I would write some quick tests to verify the behavior of the API.

The advantage of Heroku is that it is very simple and very scalable as requirements increase. While it may be more expensive than self-hosted solutions, the simplicity is well worth it.
