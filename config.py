from pymongo import MongoClient
import os
from flask import Flask

app = Flask(__name__)

try:
    app.config.from_pyfile("dev_config.cfg")

    mc = MongoClient(app.config["MONGODB_URI"])
    db = mc.heroku_wcxhtdf7

    print ">>> Development configuration file loaded."
except:
    #======================================
    # Load Heroku Environment Variables
    #======================================
    app.config.update(os.environ)

    MONGO_URL = app.config["MONGODB_URI"]

    mc = MongoClient(MONGO_URL)
    db = mc.heroku_wcxhtdf7

    print ">>> Production configuration file loaded. Debug: %s" % (str(app.config["DEBUG"]))