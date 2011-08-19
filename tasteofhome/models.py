# -*- coding: utf-8 -*-
# tasteofhome.models

from google.appengine.ext import db
from yan.auth.models import DatastoreUser


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
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class TagCoursesIndex(db.Model):
    n_courses=db.IntegerProperty()
    courses=db.ListProperty(db.Key)

class TagMessagesIndex(db.Model):
    n_messages=db.IntegerProperty()
    messages=db.ListProperty(db.Key)

class User(DatastoreUser):
    avatar=db.BlobProperty()

class UserTagsIndex(db.Model):
    tags=db.ListProperty(db.Key)

class UserMouthsIndex(db.Model):
    mouths=db.ListProperty(db.Key)

class UserHandsIndex(db.Model):
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

