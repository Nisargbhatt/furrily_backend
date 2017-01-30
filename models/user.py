"""
user model, contains documents releted to user
"""
from datetime import datetime

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine import StringField, IntField, EmbeddedDocumentField, ListField, DateTimeField
from mongoengine import BooleanField
from mongoengine import GenericReferenceField
from passlib.apps import custom_app_context as pwd_context

class UserCart(DynamicDocument):
    user = GenericReferenceField()
    gig = GenericReferenceField()


class UserWishList(DynamicDocument):
    user = GenericReferenceField()
    gig = GenericReferenceField()

class UserRatings(DynamicDocument):
    """
    This is for storing feedback given to client or seller
    """
    count = IntField()
    feedback = StringField()
    client = GenericReferenceField()
    gig = GenericReferenceField()

class UserPortfolio(EmbeddedDocument):
    """
    This is for storing portfolio of user
    """
    title = StringField()
    image = ListField()
    attachments = ListField()
    description = StringField(default=None)
    date = DateTimeField(default=datetime.now())
    skills = ListField()

class ProfileLinks(EmbeddedDocument):
    """
    This is used for storing the portfolio links that user gives
    """
    platform = StringField()
    url = StringField()



class User(DynamicDocument):
    """
    Here all the basic user details like name, email etc will be stored
    """
    firstname = StringField()
    lastname = StringField()
    email = StringField(unique=True)
    password = StringField()
    profilePicture = StringField(default="http://www.lovemarks.com/wp-content/uploads/profile-avatars/default-avatar.png")
    average_ratings = IntField()
    postings_count = IntField()
    notification_count = IntField()
    address = StringField()
    country = StringField()
    city = StringField()
    state = StringField()
    zipcode = StringField()
    portfolioLinks = ListField(EmbeddedDocumentField(ProfileLinks), default=[])
    portfolio = ListField(EmbeddedDocumentField(UserPortfolio), default=[])
    profileCompleteness = IntField(default=45)
    bio = StringField()
    langauges = ListField()
    skills = ListField(default=[])

    def encrypt_set_password(self, password):
        self.password = pwd_context.encrypt(password)


    @staticmethod
    def authenticate(email, password):
        user = User.objects(email = email).first()
        user.id = str(user.id)
        if pwd_context.verify(password, user.password):
            return user
        return None

    @staticmethod
    def identity(payload):
        user = User.objects(id=payload["identity"]).first()
        user.id = str(user.id)
        return user

