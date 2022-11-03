import mongoengine as me 
from slugify import slugify
from utils import *

class User(me.Document):
    _id = me.IntField()
    slug = me.StringField(unique=True)
    firstName = me.StringField(max_length=50, required = True)
    lastName = me.StringField(max_length=50, required= True)
    email = me.StringField(required=True, unique=True)
    phoneNumber = me.StringField(max_length=12)
    password = me.StringField(min_length=8, required=True)
    likes = me.IntField()
    profilePicture = me.ImageField()
    registrationDate = me.DateField()

    def create_slug(self):
        string_to_slugify = self.firstName + self.lastName
        slug = slugify(string_to_slugify + " " + get_random())
        self.slug = slug

class Category(me.Document):
    _id = me.IntField()
    name = me.StringField(unique=True)

class Article(me.Document):
    _id = me.IntField()
    title = me.StringField(required=True)
    author = me.ReferenceField(User, required=True)
    category = me.ReferenceField(Category, required=True)
    uploadDate = me.DateField()
    articleImage = me.ImageField()
    text = me.StringField()
    slug = me.StringField(unique=True)

    def create_slug(self):
        string_to_slugify = self.title
        slug = slugify(string_to_slugify + " " + get_random())
        self.slug = slug




