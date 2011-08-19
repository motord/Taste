# -*- coding: utf-8 -*-

"""
Kay authentication urls.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/login', endpoint='login', view='yan.auth.views.login'),
    Rule('/login_box', endpoint='login_box', view='yan.auth.views.login_box'),
    Rule('/post_session', endpoint='post_session',
         view='yan.auth.views.post_session'),
    Rule('/logout', endpoint='logout', view='yan.auth.views.logout'),
    Rule('/change_password', endpoint='change_password',
         view=('yan.auth.views.ChangePasswordHandler',(), {})),
    Rule('/request_reset_password', endpoint='request_reset_password',
         view='yan.auth.views.request_reset_password'),
    Rule('/reset_password/<session_key>', endpoint='reset_password',
         view='yan.auth.views.reset_password'),
  )
]
