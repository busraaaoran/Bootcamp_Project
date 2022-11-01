from datetime import datetime
from email import message
from flask import Flask, request, session
from flask_mongoengine import MongoEngine
from models import *
from flask_restful import Api, Resource, abort
import os

db = MongoEngine()
app = Flask(__name__)
#defining a secret key is mandatory step for using sessions in flask
app.secret_key = os.getenv("SECRET_KEY")
#Database configuration for connecting MongoDB with our Flask app
app.config['MONGODB_SETTINGS'] = [{
   
    "db": "blogDb",
    "host" : "localhost",
    "port": 27017,
    
}]

db.init_app(app)


@app.route("/")
def hello():
    categories = Category.objects(name="Travel").first()
    return f"<p>{categories.name}</p>"


class ArticlesController(Resource):
    def get(self):
        articles = Article.objects()
        if not articles:
            abort(404,message="Sorry but there is no article here")
        return articles, 200
    
    def post(self):
        data = request.get_json()
        data['uploadDate'] = datetime.utcnow()
        new_article = Article(data['title'], data['author'], data['category'], data['uploadDate'], data['articleImage'], data['text'])
        new_article.save()

        return new_article, 201

    def put(self):
        pass


    def delete(self):
        pass


class UsersController(Resource):
    def get(self):
        users = User.objects()
        if not users:
            abort(404, message="Sorry but there is no user registered to the database!")
        return users, 200
    
    def post(self):
        data = request.get_json()
        data['registrationDate'] = datetime.utcnow()
        new_user = User(data['firstname'], data['lastname'], data['email'],data['phoneNumber'],data['password'],data['likes'], data['profilePicture'],data['registrationDate']).save()

        return new_user, 201

    def put(self):
        pass

    def delete(self):
        pass


class CategoriesController(Resource):
    def get(self):
        categories = Category.objects()
        if not categories:
            abort(404,message="Sorry there is no category yet!")

        return categories
"""
category = Category()
category.name = "Makeup"
category.save()
"""