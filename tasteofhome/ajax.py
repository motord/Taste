# -*- coding: utf-8 -*-
# __author__ = 'peter'

from kay.utils import render_json_response
from yan.auth.decorators import login_required
from decorators import with_tag

@login_required
@with_tag
def markmap(request, tag):
    user=request.user
    user.add_tag(tag)
    return render_json_response(tag)





