# -*- coding: utf-8 -*-

"""
Kay authentication form.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
import itertools

import logging

from kay.i18n import lazy_gettext as _
from kay.utils.forms.modelform import ModelForm
from kay.utils import forms
from kay.utils.validators import ValidationError
from models import Tag, Course, Message, User, TagCoursesIndex
from kay.utils.forms import Field, Widget, html
from werkzeug import escape
from kay.utils.datastructures import missing
from google.appengine.ext import db
from google.appengine.api import memcache

class LabelWidget(Widget):
    def __init__(self, field, name, value, all_errors):
        super(LabelWidget, self).__init__(field, name, value, all_errors)

    def render(self, **attrs):
        return html.label(escape(self.value), **attrs)

class LinkWidget(Widget):
    def __init__(self, field, name, value, all_errors):
        super(LinkWidget, self).__init__(field, name, value, all_errors)

    def render(self, **attrs):
        return html.label(escape(self.value), **attrs)


class TagField(Field):
    def __init__(self, label=None, help_text=None, validators=None, widget=LabelWidget, messages=None, default=missing, required=False):
        super(TagField, self).__init__(label, help_text, validators, widget, messages, default)

    def convert(self, value):
        return value


class UserField(Field):
    def __init__(self, label=None, help_text=None, validators=None, widget=LabelWidget, messages=None, default=missing, required=False):
        super(UserField, self).__init__(label, help_text, validators, widget, messages, default)

    def convert(self, value):
        return value

class CRUD:
    Create, Read, Update, Delete = range(4)

class CourseForm(ModelForm):
    title=forms.TextField(required=True, min_length=3, max_length=100, label=_(u'名称'))
    content=forms.TextField(required=True, min_length=3, max_length=1000, label=_(u'描述'), widget=forms.Textarea)
    avatar=forms.FileField(label=_(u'图片'))
    owner=UserField(required=True, label=_(u'掌柜'))
    mouth=forms.BooleanField(label=_(u'想吃'))
    hand=forms.BooleanField(label=_(u'会做'))
    tag=TagField(required=True, label=_(u'属地'))
    class Meta:
        model = Course
        fields = ('title', 'content', 'avatar', 'owner')

    def save(self, commit=True, crud=CRUD.Create, **kwargs):
        def create_course():
            tag=self['tag']
            kwargs['parent']=tag
            course=super(CourseForm, self).save(commit, **kwargs)
            tag.add_course(course)
            return course
        def update_course():
            return super(CourseForm, self).save(commit, **kwargs)
        if crud==CRUD.Create:
            course=db.run_in_transaction(create_course)
        elif crud==CRUD.Update:
            course=db.run_in_transaction(update_course)
        memcache.set(course.key(), course)
        return course


class DiscussionForm(ModelForm):
    title=forms.TextField(required=True, min_length=3, max_length=100, label=_(u'讨论主题'))
    content=forms.TextField(required=True, min_length=3, max_length=1000, label=_(u'内容'), widget=forms.Textarea)
    owner=UserField(required=True, label=_(u'楼主'))
    tag=forms.ModelField(model=Tag, required=True, label=_(u'分类'), query=Tag.all().filter('depth =',100))
    class Meta:
        model = Course
        fields = ('title', 'content', 'owner')

    def save(self, commit=True, crud=CRUD.Create, **kwargs):
        def create_discussion():
            tag=self['tag']
            kwargs['parent']=tag
            discussion=super(DiscussionForm, self).save(commit, **kwargs)
            tag.add_course(discussion)
            return discussion
        def update_discussion():
            return super(DiscussionForm, self).save(commit, **kwargs)
        if crud==CRUD.Create:
            discussion=db.run_in_transaction(create_discussion)
        elif crud==CRUD.Update:
            discussion=db.run_in_transaction(update_discussion)
        memcache.set(discussion.key().__str__(), discussion)
        return discussion

class DiscussionEditForm(ModelForm):
    title=forms.TextField(required=True, min_length=3, max_length=100, label=_(u'讨论主题'))
    content=forms.TextField(required=True, min_length=3, max_length=1000, label=_(u'内容'), widget=forms.Textarea)
    owner=UserField(required=True, label=_(u'楼主'))
    tag=TagField(required=True, label=_(u'分类'))
    class Meta:
        model = Course
        fields = ('title', 'content', 'owner')

    def save(self, commit=True, crud=CRUD.Create, **kwargs):
        def create_discussion():
            tag=self['tag']
            kwargs['parent']=tag
            discussion=super(DiscussionForm, self).save(commit, **kwargs)
            tag.add_course(discussion)
            return discussion
        def update_discussion():
            return super(DiscussionForm, self).save(commit, **kwargs)
        if crud==CRUD.Create:
            discussion=db.run_in_transaction(create_discussion)
        elif crud==CRUD.Update:
            discussion=db.run_in_transaction(update_discussion)
        memcache.set(discussion.key().__str__(), discussion)
        return discussion

class MessageForm(ModelForm):
    in_reply_to=forms.TextField(required=True, min_length=3, max_length=100, label=_(u'讨论主题'))
    message=forms.TextField(required=True, min_length=3, max_length=1000, label=_(u'内容'), widget=forms.Textarea)
    author=UserField(required=True, label=_(u'楼主'))
    course=forms.ModelField(model=Course, required=True, label=_(u'讨论主题'), query=Tag.all().filter('depth =',100))
    class Meta:
        model = Message
        fields = ('in_reply_to', 'message', 'author')

    def save(self, commit=True, crud=CRUD.Create, **kwargs):
        def create_message():
            course=self['course']
            kwargs['parent']=course
            message=super(MessageForm, self).save(commit, **kwargs)
            course.add_message(message)
            return message
        def update_message():
            return super(MessageForm, self).save(commit, **kwargs)
        if crud==CRUD.Create:
            message=db.run_in_transaction(create_message)
        elif crud==CRUD.Update:
            message=db.run_in_transaction(update_message)
        memcache.set(message.key(), message)
        return message