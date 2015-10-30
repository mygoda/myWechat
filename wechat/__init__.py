# -*- coding: UTF-8 -*-
# __author__ = xutao
import os

import redis

from flask import Flask

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


wechat = None
try:
    wechat = MyCachedWechatBasic(app=wechat_app, r=r)
except(Exception,):
    pass

from . import wechat_public


class WechatCodeNeedException(Exception):
    def __init__(self, url, from_number=None):
        self.url = url
        self.from_number = from_number