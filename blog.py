from flask import Flask
from flask_mongoengine import MongoEngine
from models import *


db = MongoEngine()
app = Flask(__name__)

#Database configuration for connecting MongoDB with our Flask app
app.config['MONGODB_SETTINGS'] = [{
   
    "db": "blogDb",
    "host" : "localhost",
    "port": 27017,
    
}]

db.init_app(app)


@app.route("/")
def hello():
    return "<p>Hello Canıms</p>"


category = Category()
category.name = "Travel"
category.save()