# -*- coding: utf-8 -*-
# tasteofhome.models

from google.appengine.ext import db
from yan.auth.models import DatastoreUser
from google.appengine.api import memcache
from google.appengine.ext import deferred

# Create your models here.
class User(DatastoreUser):
    avatar=db.BlobProperty()
    mobile=db.StringProperty()

    def add_tag(self, tag):
        userTagsIndex=UserTagsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userTagsIndex:
            userTagsIndex=UserTagsIndex(parent=self)
        if userTagsIndex.tags.count(tag.key())==0:
            userTagsIndex.n_tags +=1
            userTagsIndex.tags.append(tag.key())
            userTagsIndex.put()
            memcache.set(self.key().__str__()+'::tags', Tag.get(userTagsIndex.tags))
        def add_course_tag():
            for course in self.get_mouths():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.mouths.count(self.key())==0:
                    courseUsersIndex.n_mouths +=1
                    courseUsersIndex.mouths.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))
            for course in self.get_hands():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.hands.count(self.key())==0:
                    courseUsersIndex.n_hands +=1
                    courseUsersIndex.hands.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::hands', User.get(courseUsersIndex.hands))
        deferred.defer(add_course_tag)

    def get_tags(self):
        tags=memcache.get(self.key().__str__()+'::tags')
        if tags:
            return tags
        else:
            userTagsIndex=UserTagsIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not userTagsIndex:
                userTagsIndex=UserTagsIndex(parent=self)
                return None
            tags=Tag.get(userTagsIndex.tags)
            memcache.set(self.key().__str__()+'::tags', tags)
            return tags

    def remove_tag(self, tag):
        userTagsIndex=UserTagsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userTagsIndex:
            userTagsIndex=UserTagsIndex(parent=self)
        try:
            userTagsIndex.tags.remove(tag.key())
            userTagsIndex.n_tags -=1
            userTagsIndex.put()
            memcache.set(self.key().__str__()+'::tags', Tag.get(userTagsIndex.tags))
        except ValueError:
            raise ValueError('%s not in %s\'s tags', (tag, self))
        def remove_course_tag():
            for course in self.get_mouths():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                try:
                    courseUsersIndex.mouths.remove(self.key())
                    courseUsersIndex.n_mouths -=1
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))
                except ValueError:
                    raise ValueError('%s not in %s\'s mouths', (self, course))
            for course in self.get_hands():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                try:
                    courseUsersIndex.hands.remove(self.key())
                    courseUsersIndex.n_hands -=1
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::hands', User.get(courseUsersIndex.hands))
                except ValueError:
                    raise ValueError('%s not in %s\'s hands', (self, course))
        deferred.defer(remove_course_tag)

    def add_mouth(self, course):
        userMouthsIndex=UserMouthsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userMouthsIndex:
            userMouthsIndex=UserMouthsIndex(parent=self)
        if userMouthsIndex.mouths.count(course.key())==0:
            userMouthsIndex.n_mouths +=1
            userMouthsIndex.mouths.append(course.key())
            userMouthsIndex.put()
            memcache.set(self.key().__str__()+'::mouths', userMouthsIndex.mouths)
        def add_course_mouth():
            for tag in self.get_tags():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.mouths.count(self.key())==0:
                    courseUsersIndex.n_mouths +=1
                    courseUsersIndex.mouths.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))
        deferred.defer(add_course_mouth)

    def get_mouths(self):
        mouths=memcache.get(self.key().__str__()+'::mouths')
        if mouths:
            return mouths
        else:
            userMouthsIndex=UserMouthsIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not userMouthsIndex:
                userMouthsIndex=UserMouthsIndex(parent=self)
                return None
            mouths=Course.get(userMouthsIndex.mouths)
            memcache.set(self.key().__str__()+'::mouths', mouths)
            return mouths

    def remove_mouth(self, mouth):
        userMouthsIndex=UserMouthsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userMouthsIndex:
            userMouthsIndex=UserMouthsIndex(parent=self)
        try:
            userMouthsIndex.mouths.remove(mouth.key())
            userMouthsIndex.n_mouths -=1
            userMouthsIndex.put()
            memcache.set(self.key().__str__()+'::mouths', Course.get(userMouthsIndex.mouths))
        except ValueError:
            raise ValueError('%s not in %s\'s mouths', (mouth, self))
        def remove_course_mouth():
            for tag in self.get_tags():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", mouth, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=mouth, tag=tag)
                try:
                    courseUsersIndex.mouths.remove(self.key())
                    courseUsersIndex.n_mouths -=1
                    courseUsersIndex.put()
                    memcache.set(mouth.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))
                except ValueError:
                    raise ValueError('%s not in %s\'s mouths', (self, mouth))
        deferred.defer(remove_course_mouth)

    def add_hand(self, course):
        userHandsIndex=UserHandsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userHandsIndex:
            userHandsIndex=UserHandsIndex(parent=self)
        if userHandsIndex.hands.count(course.key())==0:
            userHandsIndex.n_hands +=1
            userHandsIndex.hands.append(course.key())
            userHandsIndex.put()
            memcache.set(self.key().__str__()+'::hands', userHandsIndex.hands)
        def add_course_hand():
            for tag in self.get_tags():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.hands.count(self.key())==0:
                    courseUsersIndex.n_hands +=1
                    courseUsersIndex.hands.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::hands', User.get(courseUsersIndex.hands))
        deferred.defer(add_course_hand)

    def get_hands(self):
        hands=memcache.get(self.key().__str__()+'::hands')
        if hands:
            return hands
        else:
            userHandsIndex=UserHandsIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not userHandsIndex:
                userHandsIndex=UserHandsIndex(parent=self)
                return None
            hands=Course.get(userHandsIndex.hands)
            memcache.set(self.key().__str__()+'::hands', hands)
            return hands

    def remove_hand(self, hand):
        userHandsIndex=UserHandsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userHandsIndex:
            userHandsIndex=UserHandsIndex(parent=self)
        try:
            userHandsIndex.hands.remove(hand.key())
            userHandsIndex.n_hands -=1
            userHandsIndex.put()
            memcache.set(self.key().__str__()+'::hands', Course.get(userHandsIndex.hands))
        except (ValueError):
            raise ValueError('%s not in %s\'s hands', (hand, self))
        def remove_course_hand():
            for tag in self.get_tags():
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", hand, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=hand, tag=tag)
                try:
                    courseUsersIndex.hands.remove(self.key())
                    courseUsersIndex.n_hands -=1
                    courseUsersIndex.put()
                    memcache.set(hand.key().__str__()+'::'+tag.key().__str__()+'::hands', User.get(courseUsersIndex.hands))
                except ValueError:
                    raise ValueError('%s not in %s\'s hands', (self, hand))
        deferred.defer(remove_course_hand)

    def add_bookmark(self, message):
        userBookmarksIndex=UserBookmarksIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userBookmarksIndex:
            userBookmarksIndex=UserBookmarksIndex(parent=self)
        if userBookmarksIndex.bookmarks.count(message.key())==0:
            userBookmarksIndex.n_bookmarks +=1
            userBookmarksIndex.bookmarks.append(message.key())
            userBookmarksIndex.put()
            memcache.set(self.key().__str__()+'::bookmarks', userBookmarksIndex.bookmarks)

    def get_bookmarks(self):
        bookmarks=memcache.get(self.key().__str__()+'::bookmarks')
        if bookmarks:
            return bookmarks
        else:
            userBookmarksIndex=UserBookmarksIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not userBookmarksIndex:
                userBookmarksIndex=UserBookmarksIndex(parent=self)
                return None
            bookmarks=Message.get(userBookmarksIndex.bookmarks)
            memcache.set(self.key().__str__()+'::bookmarks', bookmarks)
            return bookmarks

    def remove_bookmark(self, bookmark):
        userBookmarksIndex=UserBookmarksIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userBookmarksIndex:
            userBookmarksIndex=UserBookmarksIndex(parent=self)
        try:
            userBookmarksIndex.bookmarks.remove(bookmark.key())
            userBookmarksIndex.n_bookmarks -=1
            userBookmarksIndex.put()
            memcache.set(self.key().__str__()+'::bookmarks', Message.get(userBookmarksIndex.bookmarks))
        except (ValueError):
            raise ValueError('%s not in %s\'s bookmarks', (bookmark, self))


class UserTagsIndex(db.Model):
    n_tags=db.IntegerProperty(default=0)
    tags=db.ListProperty(db.Key)


class UserMouthsIndex(db.Model):
    n_mouths=db.IntegerProperty(default=0)
    mouths=db.ListProperty(db.Key)


class UserHandsIndex(db.Model):
    n_hands=db.IntegerProperty(default=0)
    hands=db.ListProperty(db.Key)


class UserBookmarksIndex(db.Model):
    n_bookmarks=db.IntegerProperty(default=0)
    bookmarks=db.ListProperty(db.Key)


class Course(db.Model):
    title=db.StringProperty()
    content=db.TextProperty()
    avatar=db.BlobProperty()
    owner=db.ReferenceProperty(User)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

    def update_view_count(self, n):
        memcache.incr(self.key().__str__()+'::hits', delta=n)

    def num_views(self):
        views=memcache.get(self.key().__str__()+'::hits')
        if views is not None:
            return views
        else:
            courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseMessagesIndex:
                memcache.set(self.key().__str__()+'::hits', 0)
                return 0
            memcache.set(self.key().__str__()+'::hits', courseMessagesIndex.n_views)
            return courseMessagesIndex.n_views

    def add_message(self, message):
        courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not courseMessagesIndex:
            courseMessagesIndex=CourseMessagesIndex(parent=self)
        courseMessagesIndex.n_messages += 1
        courseMessagesIndex.messages.append(message.key())
        courseMessagesIndex.put()
        memcache.set(self.key().__str__()+'::messages', courseMessagesIndex.messages)

    def num_messages(self):
        courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not courseMessagesIndex:
            return 0
        return courseMessagesIndex.n_messages
    
    def get_messages(self):
        messages=memcache.get(self.key().__str__()+'::messages')
        if messages:
            return messages
        else:
            courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseMessagesIndex:
                courseMessagesIndex=CourseMessagesIndex(parent=self)
                return None
            messages=Tag.get(CourseMessagesIndex.messages)
            memcache.set(self.key().__str__()+'::messages', messages)
            return messages

    def num_mouths(self, tag):
        mouths=memcache.get(self.key().__str__()+'::'+tag.key().__str__()+'::n_mouths')
        if mouths is not None:
            return mouths
        else:
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseUsersIndex:
                memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::n_mouths', 0)
                return 0
            memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::n_mouths', courseUsersIndex.n_mouths)
            return courseUsersIndex.n_mouths

    def get_mouths(self, tag):
        mouths=memcache.get(self.key().__str__()+'::'+tag.key().__str__()+'::mouths')
        if mouths is not None:
            return mouths
        else:
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseUsersIndex:
                courseUsersIndex=CourseUsersIndex(parent=self, tag=tag)
                return None
            mouths=User.get(courseUsersIndex.mouths)
            memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::mouths', mouths)
            return mouths

    def num_hands(self, tag):
        hands=memcache.get(self.key().__str__()+'::'+tag.key().__str__()+'::n_hands')
        if hands is not None:
            return hands
        else:
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseUsersIndex:
                memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::n_hands', 0)
                return 0
            memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::n_hands', courseUsersIndex.n_hands)
            return courseUsersIndex.n_hands

    def get_hands(self, tag):
        hands=memcache.get(self.key().__str__()+'::'+tag.key().__str__()+'::hands')
        if hands is not None:
            return hands
        else:
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not courseUsersIndex:
                courseUsersIndex=CourseUsersIndex(parent=self, tag=tag)
                return None
            hands=User.get(courseUsersIndex.hands)
            memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::hands', hands)
            return hands


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
        memcache.set(self.key().__str__()+'::courses', tagCoursesIndex.courses)

    def num_courses(self):
        tagCoursesIndex=TagCoursesIndex.gql("WHERE ANCESTOR IS :1 AND depth = :2", self, self.depth).get()
        if not tagCoursesIndex:
            return 0
        return tagCoursesIndex.n_courses

    def get_courses(self):
        courses=memcache.get(self.key().__str__()+'::courses')
        if courses:
            return courses
        else:
            tagCoursesIndex=TagCoursesIndex.gql("WHERE ANCESTOR IS :1", self).get()
            if not tagCoursesIndex:
                tagCoursesIndex=TagCoursesIndex(parent=self)
                return None
            courses=Tag.get(tagCoursesIndex.courses)
            memcache.set(self.key().__str__()+'::courses', courses)
            return courses
    

class CourseUsersIndex(db.Model):
    tag=db.ReferenceProperty(Tag)
    n_mouths=db.IntegerProperty(default=0)
    n_hands=db.IntegerProperty(default=0)
    mouths=db.ListProperty(db.Key)
    hands=db.ListProperty(db.Key)


class TagCoursesIndex(db.Model):
    depth=db.IntegerProperty()
    n_courses=db.IntegerProperty(default=0)
    courses=db.ListProperty(db.Key)

    
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
    message=db.TextProperty()
    author=db.ReferenceProperty(User)
    created=db.DateTimeProperty(auto_now_add=True)
    updated=db.DateTimeProperty(auto_now=True)

