# -*- coding: utf-8 -*-
# __author__ = 'peter'

from mapreduce import operation as op
from models import CourseMessagesIndex
from google.appengine.api import memcache

def update_view_count(entity):
    courseMessagesIndex=CourseMessagesIndex.gql("WHERE ANCESTOR IS :1", entity).get()
    if not courseMessagesIndex:
        courseMessagesIndex=CourseMessagesIndex(parent=entity)
    views=memcache.get(entity.key().__str__()+'hits')
    if views is not None:
        if views>courseMessagesIndex.n_views:
            courseMessagesIndex.n_views=views
            yield op.db.Put(courseMessagesIndex)
    memcache.set(entity.key().__str__()+'hits', courseMessagesIndex.n_views)
