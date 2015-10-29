# -*- coding: UTF-8 -*-
# __author__ = xutao


from flask.ext.script import Manager
from wechat import wechat_app

wechat_app.debug = True
manager = Manager(app=wechat_app)