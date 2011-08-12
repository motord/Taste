# -*- coding: utf-8 -*-
# tasteofhome.models

from google.appengine.ext import db
from kay.auth.models import DatastoreUser


# Create your models here.
class Course(db.Model):
    name=db.StringProperty()
    description=db.StringProperty()
    avatar=db.BlobProperty()
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class Tag(db.Model):
    name=db.StringProperty()
    depth=db.IntegerProperty()
    courses=db.ListProperty(db.Key)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class User(DatastoreUser):
    avatar=db.BlobProperty()
    tags=db.ListProperty(db.Key)
    mouths=db.ListProperty(db.Key)
    hands=db.ListProperty(db.Key)

class Feast(db.Model):
    schedule=db.DateTimeProperty()
    tag=db.ReferenceProperty(Tag)
    courses=db.ListProperty(db.Key)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class Message(db.Model):
    message=db.StringProperty()
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

