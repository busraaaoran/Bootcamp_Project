from datetime import datetime
from flask import Flask, jsonify, request, session
from flask_mongoengine import MongoEngine
from models import *
from flask_restful import Api, Resource, abort, marshal_with, fields
import os
import json
from serializer import Serializer

db = MongoEngine()
app = Flask(__name__)
api = Api(app)
ser = Serializer(app)
#defining a secret key is mandatory step for using sessions in flask
app.secret_key = os.getenv("SECRET_KEY")
#Database configuration for connecting MongoDB with our Flask app
app.config['MONGODB_SETTINGS'] = [{
   
    "db": "blogDb",
    "host" : "localhost",
    "port": 27017,
    
}]

db.init_app(app)

category_fields = {
    '_id': fields.String,
    'name': fields.String,
}

@app.route("/")
def hello():
    categories = User.objects(slug='hamza-oran-0392c94e').first()
    return f"<p>{categories.firstName}</p>"


class ArticlesController(Resource):
    def get(self):
        articles = Article.objects().to_json()
        if len(articles) == 0:
            print("333")
            abort(404,message="Sorry but there is no article here")
        return articles, 200
    
    def post(self):
        data = request.get_json()
        data['uploadDate'] = datetime.utcnow()
        new_article = Article(data['title'], data['author'], data['category'], data['uploadDate'], data['articleImage'], data['text'])
        new_article.save()

        return new_article, 201

    def put(self, article_id):
        data = request.get_json(force=True)
        Article.objects().get(_id=article_id).update(**data)
        return "", 204

    #formatted string should be fixed
    def delete(self, slug):
        Article.objects(slug=slug).delete()
        return f"Article with {slug} id number is deleted!", 204


class UsersController(Resource):
    def get(self):
        users = User.objects().to_json()
        if not users:
            abort(404, message="Sorry but there is no user registered to the database!")
        return users, 200
    
    def post(self):
        data = request.get_json(force=True)
        #data['profilePicture'] = ""
        data['registrationDate'] = datetime.utcnow()
        data['slug'] = create_slug(data['firstName'],data['lastName'])
        new_user = User(**data).save()
        id = new_user.id

        return {'id':str(id)}, 201



    def put(self, user_id):
        data = request.get_json(force=True)
        User.objects().get(_id=user_id).update(**data)
        return "",204

    def delete(self, user_id):
        User.objects.get(_id=user_id).delete()
        return f"User with {user_id} id number deleted!", 204

class SingleUserView(Resource):

    def get(self, slug):
        user = User.objects(slug=slug).first().to_json()
        if not user:
            abort(404, message="Sorry but there is no such user registered to the database!")
        return user, 200
    
    def post(self):
        data = request.get_json(force=True)
        #data['profilePicture'] = ""
        data['registrationDate'] = datetime.utcnow()
        data['slug'] = create_slug(data['firstName'],data['lastName'])
        new_user = User(**data).save()
        id = new_user.id

        return {'id':str(id)}, 201

    ##TRY TO SOLVE THIS ISSUE FIRST!!!
    def put(self, user_id):
        data = request.get_json(force=True)
        if data['firstName']:
            User.objects().get(_id=user_id).update(firstName=data['firstName'])
        if data['lastName']:
            User.objects().get(_id=user_id).update(lastName=data['lastName'])
        if data['phoneNumber']:
            User.objects().get(_id=user_id).update(phoneNumber=data['phoneNumber'])
        if data['password']:
            User.objects().get(_id=user_id).update(password=data['password'])
        if data['likes']:
            User.objects().get(_id=user_id).update(likes=data['likes'])
        return "",204

    def delete(self, user_id):
        User.objects().get(_id=user_id).first().delete()
        return f"User with {user_id} id number deleted!", 204

class SingleArticleView(Resource):
    def get(self,slug):
        article = Article.objects(slug=slug).first().to_json()
        if not article:
            abort(404,message="Sorry but there is no such article here")
        return article, 200
    
    def post(self):
        data = request.get_json()
        data['uploadDate'] = datetime.utcnow()
        data['slug'] = create_article_slug(data['title'])
        new_article = Article(**data).save()

        return new_article, 201

    def put(self, slug):
        data = request.get_json(force=True)
        Article.objects().get(slug=slug).update(**data)
        return "", 204

    def delete(self, slug):
        article = Article.objects().get(slug=slug).first()
        article_name = article.title
        article.delete()
        return f"Article {article_name} is deleted!", 204

class CategoriesController(Resource):

    def get(self):
        categories = Category.objects().to_json()
        if not categories:
            abort(404,message="Sorry there is no category yet!")
        return categories, 200
    
    def post(self):
        data = request.get_json()
        new_category = Category(**data).save()
        print(new_category)
        return new_category.to_json(), 201
    


api.add_resource(UsersController, '/users')
api.add_resource(ArticlesController, '/articles')
api.add_resource(CategoriesController, '/categories')
api.add_resource(SingleUserView, '/users/<string:slug>')
api.add_resource(SingleArticleView, '/articles/<string:slug>')

'''
category = Category()
category.name = "Travel"
category.save()
'''