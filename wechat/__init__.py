# -*- coding: UTF-8 -*-
# __author__ = xutao
import os

import redis
import urllib
from flask import Flask, current_app, redirect

from wechat.setting import Config
from wechat.lib.log import configure_log


# 实例化 wechat app
from wechat.lib.wechat import MyCachedWechatBasic

wechat_app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

wechat_app.config.from_object(Config)

# log 配置
path = '%s/wechat/log.yaml' % BASE_DIR
configure_log(wechat_app, path)

# redis

config = wechat_app.config

r = redis.StrictRedis(host=config.get('REDIS_HOST'), port=config.get('REDIS_PORT'),
                      password=config.get('REDIS_PASSWORD'))


# 实例化微信处理类

wechat = None
try:
    wechat = MyCachedWechatBasic(app=wechat_app, r=r)
except(Exception,):
    pass

from . import wechat_public


if wechat:
    from wechat.wechat_public import wechat_bp

    wechat_app.register_blueprint(wechat_bp, url_prefix='/wechat')