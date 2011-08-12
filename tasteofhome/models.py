# -*- coding: utf-8 -*-
# tasteofhome.models

from ndb import model


# Create your models here.
class Course(model.Model):
    name=model.StringProperty()
    description=model.StringProperty()
    avatar=model.BlobProperty()
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Tag(model.Model):
    name=model.StringProperty()
    depth=model.IntegerProperty()
    courses=model.StructuredProperty(Course, repeated=True)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class User(model.Model):
    username=model.StringProperty()
    email=model.StringProperty()
    avatar=model.BlobProperty()
    mouths=model.StructuredProperty(Course, repeated=True)
    hands=model.StructuredProperty(Course, repeated=True)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Feast(model.Model):
    schedule=model.DateTimeProperty()
    tag=model.StructuredProperty(Tag)
    courses=model.StructuredProperty(Course, repeated=True)
    users=model.StructuredProperty(User, repeated=True)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Message(model.Model):
    message=model.StringProperty()
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

