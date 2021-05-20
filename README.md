# amazon-price-alert
Note that this is just a demo program.

This program notices when the price of the user inputted item has been changed.

Prices of all items are stored in your MongoDB database. The price is checked every 5 minutes and if it has been changed, a notification is printed in the console, and database information is updated.

# Requirements
Install Scrapy with pip:
`pip install scrapy`

To use Scrapy-Splash, first, you need to install Splash. Follow the link to do so: https://splash.readthedocs.io/en/stable/install.html.
Then, install Scrapy-Splash:
`pip install scrapy-splash`

Note, that when using the scraper, you MUST always have a running container of docker: `sudo docker run -it -p 8050:8050 --rm scrapinghub/splash`

To use PyMongo, install MongoDB: https://docs.mongodb.com/manual/installation/. 

Then install PyMongo with pip: `pip install pymongo`


# How to use
Go to the `user_input.py` file. `AMAZON_URLS` should contain a list of URLs for which you want prices to be tracked. `MONGO_URI` is your mongo URI. `MONGO_DATABASE` is the name of the database. `COLLECTION` is the name of the collection.

After that, run the `scheduler.py` file. It will run continuously. 

If you want to change the delay of a wait between checking the price, on line 35 in `scheduler.py` edit `300` with any desired value (in seconds).
