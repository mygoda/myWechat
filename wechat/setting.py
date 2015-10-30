# -*- coding: UTF-8 -*-
# __author__ = xutao


class Config(object):

    SECRET_KEY = '1234567890123'

    WECHAT_APP_TOKEN = u'testtest'

    WECHAT_APP_REPLY_TEMPLATE = u'-9uUqA6B_QPQ-TGlhAvKMMr1WTPmxELKK479WLHSiZA'

    WECHAT_APP_ID = u'wxea72f3579541a695'

    WECHAT_APP_SECRET = u'24416aeb2dcaea8be48a467a57bf04fa'

    WECHAT_ACCESS_TOKEN_KEY = u'wechat:access_token'

    WECHAT_OAUTH2_URL = u'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + WECHAT_APP_ID \
                        + u'&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''
    REDIS_URL = 'redis://:{password}@{host}:{port}'.format(password=REDIS_PASSWORD, host=REDIS_HOST, port=REDIS_PORT)

    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'wall-e@ihaoyisheng.com'
    MAIL_PASSWORD = 'ihaoyisheng123'
    ADMINS = ['18346552658@163.com']