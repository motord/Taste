# -*- coding: utf-8 -*-
# tasteofhome.models

from google.appengine.ext import db
from yan.auth.models import DatastoreUser


# Create your models here.
class User(DatastoreUser):
    avatar=db.BlobProperty()

class Course(db.Model):
    title=db.StringProperty()
    content=db.StringProperty()
    avatar=db.BlobProperty()
    owner=db.ReferenceProperty(User)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class CourseMessagesIndex(db.Model):
    n_messages=db.IntegerProperty()
    messages=db.ListProperty(db.Key)

class Tag(db.Model):
    name=db.StringProperty()
    depth=db.IntegerProperty()
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class TagCoursesIndex(db.Model):
    n_courses=db.IntegerProperty(default=0)
    courses=db.ListProperty(db.Key)

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

class Prospect(db.Model):
    tag=db.ReferenceProperty(Tag)
    courses=db.ListProperty(db.Key)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class Notification(db.Model):
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

class Message(db.Model):
    in_reply_to=db.SelfReferenceProperty()
    message=db.StringProperty()
    author=db.ReferenceProperty(User)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

