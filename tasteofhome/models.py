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
        deferred.defer(self.add_course_tag, tag)

    def add_course_tag(self, tag):
        mouths=self.get_mouths()
        if mouths:
            for course in mouths:
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.mouths.count(self.key())==0:
                    courseUsersIndex.n_mouths +=1
                    courseUsersIndex.mouths.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))
        hands=self.get_hands()
        if hands:
            for course in hands:
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.hands.count(self.key())==0:
                    courseUsersIndex.n_hands +=1
                    courseUsersIndex.hands.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::hands', User.get(courseUsersIndex.hands))

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
        deferred.defer(self.remove_course_tag, tag)

    def remove_course_tag(self, tag):
        mouths=self.get_mouths()
        if mouths:
            for course in mouths:
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
        hands=self.get_hands()
        if hands:
            for course in hands:
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

    def add_mouth(self, course):
        userMouthsIndex=UserMouthsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userMouthsIndex:
            userMouthsIndex=UserMouthsIndex(parent=self)
        if userMouthsIndex.mouths.count(course.key())==0:
            userMouthsIndex.n_mouths +=1
            userMouthsIndex.mouths.append(course.key())
            userMouthsIndex.put()
            memcache.set(self.key().__str__()+'::mouths', userMouthsIndex.mouths)
        deferred.defer(self.add_course_mouth, course)

    def add_course_mouth(self, course):
        tags=self.get_tags()
        if tags:
            for tag in tags:
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.mouths.count(self.key())==0:
                    courseUsersIndex.n_mouths +=1
                    courseUsersIndex.mouths.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))

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

    def remove_mouth(self, course):
        userMouthsIndex=UserMouthsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userMouthsIndex:
            userMouthsIndex=UserMouthsIndex(parent=self)
        try:
            userMouthsIndex.courses.remove(course.key())
            userMouthsIndex.n_courses -=1
            userMouthsIndex.put()
            memcache.set(self.key().__str__()+'::courses', Course.get(userMouthsIndex.courses))
        except ValueError:
            raise ValueError('%s not in %s\'s courses', (course, self))
        deferred.defer(self.remove_course_mouth, course)

    def remove_course_mouth(self, course):
        tags=self.get_tags()
        if tags:
            for tag in tags:
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                try:
                    courseUsersIndex.mouths.remove(self.key())
                    courseUsersIndex.n_mouths -=1
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::mouths', User.get(courseUsersIndex.mouths))
                except ValueError:
                    raise ValueError('%s not in %s\'s courses', (self, course))

    def add_hand(self, course):
        userHandsIndex=UserHandsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userHandsIndex:
            userHandsIndex=UserHandsIndex(parent=self)
        if userHandsIndex.hands.count(course.key())==0:
            userHandsIndex.n_hands +=1
            userHandsIndex.hands.append(course.key())
            userHandsIndex.put()
            memcache.set(self.key().__str__()+'::hands', userHandsIndex.hands)
        deferred.defer(self.add_course_hand, course)

    def add_course_hand(self, course):
        tags=self.get_tags()
        if tags:
            for tag in tags:
                courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", course, tag)
                if not courseUsersIndex:
                    courseUsersIndex=CourseUsersIndex(parent=course, tag=tag)
                if courseUsersIndex.hands.count(self.key())==0:
                    courseUsersIndex.n_hands +=1
                    courseUsersIndex.hands.append(self.key())
                    courseUsersIndex.put()
                    memcache.set(course.key().__str__()+'::'+tag.key().__str__()+'::hands', User.get(courseUsersIndex.hands))

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

    def remove_hand(self, course):
        userHandsIndex=UserHandsIndex.gql("WHERE ANCESTOR IS :1", self).get()
        if not userHandsIndex:
            userHandsIndex=UserHandsIndex(parent=self)
        try:
            userHandsIndex.hands.remove(course.key())
            userHandsIndex.n_hands -=1
            userHandsIndex.put()
            memcache.set(self.key().__str__()+'::hands', Course.get(userHandsIndex.hands))
        except (ValueError):
            raise ValueError('%s not in %s\'s hands', (course, self))
        deferred.defer(self.remove_course_hand, course)

    def remove_course_hand(self, course):
        tags=self.get_tags()
        if tags:
            for tag in tags:
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
            messages=Message.get(CourseMessagesIndex.messages)
            memcache.set(self.key().__str__()+'::messages', messages)
            return messages

    def num_mouths(self, tag):
        mouths=memcache.get(self.key().__str__()+'::'+tag.key().__str__()+'::n_mouths')
        if mouths is not None:
            return mouths
        else:
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", self, tag).get()
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
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", self, tag).get()
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
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", self, tag).get()
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
            courseUsersIndex=CourseUsersIndex.gql("WHERE ANCESTOR IS :1 AND tag = :2", self, tag).get()
            if not courseUsersIndex:
                courseUsersIndex=CourseUsersIndex(parent=self, tag=tag)
                return None
            hands=User.get(courseUsersIndex.hands)
            memcache.set(self.key().__str__()+'::'+tag.key().__str__()+'::hands', hands)
            return hands

    def delete(self, **kwargs):
        def delete_course():
            messages=Message.get(CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get().messages)
            db.delete([message.key() for message in messages])
            tag=self.parent()
            tag.remove_course(self)
            courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self, keys_only=True)
            courseUsersIndexes=CourseUsersIndex.gql("WHERE ANCESTOR IS :1", self, keys_only=True)
            db.delete([courseMessagesIndex] + courseUsersIndexes)
            super(Course, self).delete(**kwargs)
        db.run_in_transaction(delete_course)
        userMouthsIndexes=UserMouthsIndex.gql("WHERE mouths = :1", self)
        for umi in userMouthsIndexes:
            umi.n_mouths -= 1
            umi.mouths.remove(self.key())
            umi.put()
        userHandsIndexes=UserHandsIndex.gql("WHERE mouths = :1", self)
        for uhi in userHandsIndexes:
            uhi.n_hands -= 1
            uhi.hands.remove(self.key())
            uhi.put()

    def move_to_tag(self, destination_tag):
        deferred.defer(self.move_course_to_tag, destination_tag)

    def move_course_to_tag(self, destination_tag):
        new_course=Course(parent=destination_tag, title=self.title, content=self.content, avatar=self.avatar, owner=self.owner)
        def clone_course():
            new_course.put()
            destination_tag.add_course(new_course)
            messages=Message.get(CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", self).get().messages)
            new_messages=[Message(parent=new_course, in_reply_to=m.in_reply_to, message=m.message, author=m.author) for m in messages]
            db.put(new_messages)
            courseMessagesIndex=CourseMessagesIndex(parent=new_course, n_views=self.num_views(), n_messages=self.n_messages(), messages=self.get_messages())
            courseMessagesIndex.put()
            db.put([CourseUsersIndex(parent=new_course, tag=destination_tag, n_mouths=self.n_mouths, n_hands=self.n_hands, mouths=self.get_mouths(cui.tag), hands=self.get_hands(cui.tag)) for cui in CourseUsersIndex.gql("WHERE ANCESTOR IS :1", self)])
        db.run_in_transaction(clone_course)
        userMouthsIndexes=UserMouthsIndex.gql("WHERE mouths = :1", self)
        for umi in userMouthsIndexes:
            umi.n_mouths += 1
            umi.mouths.append(new_course.key())
            umi.put()
        userHandsIndexes=UserHandsIndex.gql("WHERE mouths = :1", self)
        for uhi in userHandsIndexes:
            uhi.n_hands += 1
            uhi.hands.append(new_course.key())
            uhi.put()
        self.delete()

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

    def remove_course(self, course):
        tagCoursesIndex=TagCoursesIndex.gql("WHERE ANCESTOR IS :1 AND depth = :2", self, self.depth).get()
        if not tagCoursesIndex:
            tagCoursesIndex=TagCoursesIndex(parent=self, depth=self.depth)
        try:
            tagCoursesIndex.courses.remove(course.key())
            tagCoursesIndex.n_courses -= 1
            tagCoursesIndex.put()
            memcache.set(self.key().__str__()+'::courses', tagCoursesIndex.courses)
        except (ValueError):
            raise ValueError('%s not in tag %s', (course, self))


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

