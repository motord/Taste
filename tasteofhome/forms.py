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
from models import Tag, Course, Message, User
from kay.utils.forms import Field, Widget, html
from werkzeug import escape
from kay.utils.datastructures import missing

class LabelWidget(Widget):
    def __init__(self, text):
      self.text = text

    def render(self, **attrs):
        return html.label(escape(self.text), **attrs)


class TagField(Field):
    def __init__(self, label=None, help_text=None, validators=None, widget=LabelWidget, messages=None, default=missing, required=False):
        super(TagField, self).__init__(label, help_text, validators, widget, messages, default)



class UserField(Field):
    def __init__(self, label=None, help_text=None, validators=None, widget=LabelWidget, messages=None, default=missing, required=False):
        super(UserField, self).__init__(label, help_text, validators, widget, messages, default)


class CourseForm(ModelForm):
    name=forms.TextField(required=True, min_length=3, max_length=100, label=_(u'名称'))
    description=forms.TextField(required=True, min_length=3, max_length=1000, label=_(u'描述'), widget=forms.Textarea)
    avatar=forms.FileField(label=_(u'图片'))
    owner=UserField(required=True, label=_(u'掌柜'))
    mouth=forms.BooleanField(label=_(u'想吃'))
    hand=forms.BooleanField(label=_(u'会做'))
    tag=TagField(required=True, label=_(u'属地'))
    class Meta:
        model = Course
        fields = ('name', 'description', 'avatar', 'owner')
