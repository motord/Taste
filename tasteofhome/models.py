# -*- coding: utf-8 -*-
# tasteofhome.models

from google.appengine.ext import db
from yan.auth.models import DatastoreUser
from google.appengine.api import memcache


# Create your models here.
class User(DatastoreUser):
    avatar=db.BlobProperty()
    mobile=db.StringProperty()

    def add_tag(self, tag):
        userTagsIndex=UserTagsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userTagsIndex:
            userTagsIndex=UserTagsIndex(parent=self)
        userTagsIndex.n_tags +=1
        userTagsIndex.tags.append(tag)
        userTagsIndex.put()

class Course(db.Model):
    title=db.StringProperty()
    content=db.StringProperty(multiline=True)
    avatar=db.BlobProperty()
    owner=db.ReferenceProperty(User)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

    def update_view_count(self, n):
        memcache.incr(self.key().__str__()+'hits', delta=n)

    def num_views(self):
        views=memcache.get(self.key().__str__()+'hits')
        if views is not None:
            return views
        else:
            courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseMessagesIndex:
                memcache.set(self.key().__str__()+'hits', 0)
                return 0
            memcache.set(self.key().__str__()+'hits', courseMessagesIndex.n_views)
            return courseMessagesIndex.n_views

    def add_message(self, message):
        courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not courseMessagesIndex:
            courseMessagesIndex=CourseMessagesIndex(parent=self)
        courseMessagesIndex.n_messages += 1
        courseMessagesIndex.put()

    def num_messages(self):
        courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not courseMessagesIndex:
            return 0
        return courseMessagesIndex.n_messages

class CourseMessagesIndex(db.Model):
    n_views=db.IntegerProperty(default=0)
    n_messages=db.IntegerProperty(default=0)
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

    def add_course(self, course):
        tagCoursesIndex=TagCoursesIndex.gql("WHERE ANCESTOR IS :1 AND depth = :2", self, self.depth).get()
        if not tagCoursesIndex:
            tagCoursesIndex=TagCoursesIndex(parent=self, depth=self.depth)
        tagCoursesIndex.n_courses += 1
        tagCoursesIndex.courses.append(course.key())
        tagCoursesIndex.put()

    def num_courses(self):
        tagCoursesIndex=TagCoursesIndex.gql("WHERE ANCESTOR IS :1 AND depth = :2", self, self.depth).get()
        if not tagCoursesIndex:
            return 0
        return tagCoursesIndex.n_courses
    
class TagCoursesIndex(db.Model):
    depth=db.IntegerProperty()
    n_courses=db.IntegerProperty(default=0)
    courses=db.ListProperty(db.Key)

class UserTagsIndex(db.Model):
    n_tags=db.IntegerProperty(default=0)
    tags=db.ListProperty(db.Key)

class UserMouthsIndex(db.Model):
    mouths=db.ListProperty(db.Key)

class UserHandsIndex(db.Model):
    hands=db.ListProperty(db.Key)

class UserBookmarksIndex(db.Model):
    bookmarks=db.ListProperty(db.Key)

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

