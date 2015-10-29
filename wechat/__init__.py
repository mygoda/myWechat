# -*- coding: UTF-8 -*-
# __author__ = xutao
import os
import redis
from flask import Flask
from setting.setting import Config
from lib.log import configure_log

# 实例化 wechat app
from lib.wechat import MyCachedWechatBasic

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


# qiniu

from qiniu import Auth, BucketManager

q = Auth(config.get('QINIU_ACCESS_KEY'), config.get('QINIU_SECRET_KEY'))
q_token = q.upload_token(bucket='ih-data', expires=31536000)  # 一年过期
bucket = BucketManager(q)