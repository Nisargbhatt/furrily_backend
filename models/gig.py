"""
Find all the classes releated to gig here
"""

from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine import StringField, IntField, ListField, DateTimeField, ReferenceField, BooleanField


from .user import User

class Gig(DynamicDocument):
    """
    Posting for gig
    """
    title = StringField()
    description = StringField()
    price = StringField()
    attachments = ListField(default=[])
    postedBy = ReferenceField(User)
    time = IntField()
    skills = ListField()
    categories = ListField()
    successRate = IntField()

class Order(EmbeddedDocument):
    """
    All Hirings are present here
    """
    client = ReferenceField(User)
    gig = ReferenceField(Gig)
    isActive = BooleanField(default=False)
