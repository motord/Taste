# -*- coding: utf-8 -*-
# __author__ = 'peter'

from kay.ext.jsonrpc2 import JsonRpcApplication
from kay.handlers.wrapper import WsgiApplicationHandler
from yan.auth.decorators import login_required

@login_required
def markmap(request, tag):
    user=request.user
    user.add_tag(tag)
    return tag

methods = {
  "markmap": markmap,
}
rpc_application = JsonRpcApplication(methods)
rpc_handler = WsgiApplicationHandler(rpc_application)




