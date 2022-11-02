from datetime import datetime
from flask import Flask, request, session
from flask_mongoengine import MongoEngine
from models import *
from flask_restful import Api, Resource, abort, marshal_with, fields
import os

db = MongoEngine()
app = Flask(__name__)
api = Api(app)
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
    categories = User.objects(_id=1).first()
    return f"<p>{categories.firstName}</p>"


class ArticlesController(Resource):
    def get(self):
        articles = Article.objects().to_json()
        if not articles:
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

    def delete(self, article_id):
        Article.objects().get(_id=article_id).delete()
        return f"Article with {article_id} id number is deleted!", 204


class UsersController(Resource):
    def get(self):
        users = User.objects().to_json()
        if not users:
            abort(404, message="Sorry but there is no user registered to the database!")
        return users, 200
    
    def post(self):
        data = request.get_json(force=True)
        data['registrationDate'] = datetime.utcnow()
        new_user = User(**data).save()
        id = new_user._id

        return {'id':str(id)}, 201

    def put(self, user_id):
        data = request.get_json(force=True)
        User.objects().get(_id=user_id).update(**data)
        return "",204

    def delete(self, user_id):
        User.objects.get(_id=user_id).delete()
        return f"User with {user_id} id number deleted!", 204

class SingleUserView(Resource):

    def get(self, user_id):
        user = User.objects().get(_id=user_id).to_json()
        if not user:
            abort(404, message="Sorry but there is no such user registered to the database!")
        return user, 200
    
    def post(self):
        data = request.get_json(force=True)
        data['registrationDate'] = datetime.utcnow()
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
    def get(self,article_id):
        article = Article.objects().get(_id=article_id).to_json()
        if not article:
            abort(404,message="Sorry but there is no such article here")
        return article, 200
    
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

    def delete(self, article_id):
        Article.objects().get(_id=article_id).delete()
        return f"Article with {article_id} id number is deleted!", 204

class CategoriesController(Resource):

    def get(self):
        categories = Category.objects().to_json()
        if not categories:
            abort(404,message="Sorry there is no category yet!")
        return categories, 200
    
    def post(self):
        data = request.get_json()
        new_category = Category(**data).save()
        
        return new_category, 201
    


api.add_resource(UsersController, '/users')
api.add_resource(ArticlesController, '/articles')
api.add_resource(CategoriesController, '/categories')
api.add_resource(SingleUserView, '/users/<int:user_id>')
api.add_resource(SingleArticleView, '/articles/<int:article_id>')

'''
category = Category()
category.name = "Travel"
category.save()
'''