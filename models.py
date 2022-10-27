import mongoengine as me 

class User(me.Document):
    firstName = me.StringField(max_length=50, required = True)
    lastName = me.StringField(max_length=50, required= True)
    email = me.StringField(required=True, unique=True)
    phoneNumber = me.StringField(max_length=12)
    password = me.StringField(min_length=8, required=True)
    likes = me.IntField()
    profilePicture = me.ImageField()
    registrationDate = me.DateField()

class Category(me.Document):
    name = me.StringField(unique=True)

class Article(me.Document):
    title = me.StringField()
    author = me.ReferenceField(User, required=True)
    category = me.ReferenceField(Category, required=True)
    uploadDate = me.DateField()
    articleImage = me.ImageField()
    text = me.StringField()




