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
    courses=model.StructuredProperty(Course, repeated=True)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class User(model.Model):
    username=model.StringProperty()
    email=model.StringProperty()
    avatar=model.BlobProperty()
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Mouth(model.Model):
    course=model.StructuredProperty(Course)
    user=model.StructuredProperty(User)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Hand(model.Model):
    course=model.StructuredProperty(Course)
    user=model.StructuredProperty(User)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Feast(model.Model):
    schedule=model.DateTimeProperty()
    tag=model.StructuredProperty(Tag)
    mouths=model.StructuredProperty(Mouth, repeated=True)
    hands=model.StructuredProperty(Hand, repeated=True)
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Message(model.Model):
    message=model.StringProperty()
    created=model.DateTimeProperty(auto_now_add=True)
    updated=model.DateTimeProperty(auto_now=True)

class Trail(model.Model):
    user=model.StructuredProperty(User)
        