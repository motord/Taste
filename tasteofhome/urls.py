# -*- coding: utf-8 -*-
# tasteofhome.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('tasteofhome/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'tasteofhome/index': 'tasteofhome.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='tasteofhome.views.index'),
    Rule('/register', endpoint='register', view='tasteofhome.views.register'),
    Rule('/data/tags', endpoint='data.tags', view='tasteofhome.data.tags'),
    Rule('/data/forum', endpoint='data.forum', view='tasteofhome.data.forum'),
    Rule('/data/create_admin', endpoint='data.create_admin', view='tasteofhome.data.create_admin'),
    Rule('/data/fix', endpoint='data.fix', view='tasteofhome.data.fix'),
    Rule('/tag/<key>/', endpoint='tag', view='tasteofhome.views.tag'),
    Rule('/tag/<key>/p/<page>', endpoint='tag.page', view='tasteofhome.views.tag_page'),
    Rule('/course/<key>', endpoint='course', view='tasteofhome.views.course'),
    Rule('/course/<key>/p/<page>', endpoint='course.page', view='tasteofhome.views.course_page'),
    Rule('/new/course/<tag_key>', endpoint='new.course', view='tasteofhome.views.new_course'),
    Rule('/edit/course/<course_key>', endpoint='edit.course', view='tasteofhome.views.edit_course'),
    Rule('/rpc', endpoint='rpc', view='tasteofhome.rpc.rpc_handler'),
    Rule('/forum/discussions', endpoint='forum.discussions', view='tasteofhome.views.forum_discussions'),
    Rule('/forum/discussions/p/<page>', endpoint='forum.discussions.page', view='tasteofhome.views.forum_discussions_page'),
    Rule('/forum/categories/<tag_key>', endpoint='forum.category', view='tasteofhome.views.forum_category'),
    Rule('/forum/categories/<tag_key>/p/<page>', endpoint='forum.category.page', view='tasteofhome.views.forum_category_page'),
    Rule('/forum/discussion/<course_key>', endpoint='discussion', view='tasteofhome.views.forum_discussion'),
    Rule('/forum/discussion/<course_key>/p/<page>', endpoint='discussion.page', view='tasteofhome.views.forum_discussion_page'),
    Rule('/forum/new/discussion', endpoint='new.discussion', view='tasteofhome.views.new_discussion'),
    Rule('/forum/edit/discussion/<course_key>', endpoint='edit.discussion', view='tasteofhome.views.edit_discussion'),
    Rule('/user/<user_name>', endpoint='user', view='tasteofhome.views.user'),
    Rule('/termsofservice', endpoint='termsofservice', view='tasteofhome.views.termsofservice'),
    Rule('/robots.txt', endpoint='robots', view='tasteofhome.views.robots'),
    Rule('/tasks/update_view_count', endpoint='tasks.update_view_count', view='tasteofhome.tasks.update_view_count'),
  )
]

