# -*- coding: UTF-8 -*-
# __author__ = xutao

import requests
from wechat_sdk import WechatBasic
import logging


# 实例化微信类
class CachedWechatBasic(WechatBasic):
    def __init__(self, app=None, r=None):
        self.prefix = 'wechat_cache'
        self.token_key = None
        self.reply_template = None
        self.app = app
        self.r = r

        if app:
            self.init_app(app)

    def __repr__(self):
        return u"<%s: %s, %s>" % (self.__class__.__name__, self.token_key, self.reply_template)

    def __str__(self):
        return self.__repr__()

    def init_app(self, app):
        self.app = app

        config = app.config
        self.token_key = config.get('WECHAT_ACCESS_TOKEN_KEY')
        self.reply_template = config.get('WECHAT_APP_REPLY_TEMPLATE')
        self.oauth2_url = config.get('WECHAT_OAUTH2_URL')
        self.token = config.get('WECHAT_APP_TOKEN')
        self.appid = config.get('WECHAT_APP_ID')
        self.appsecret = config.get('WECHAT_APP_SECRET')

        self._auth(self.token, self.appid, self.appsecret)

        logging.info('WECHAT TOKEN: %s' % self.get_access_token())

    def _auth(self, token, appid, appsecret):
        super(CachedWechatBasic, self).__init__(token=token, appid=appid, appsecret=appsecret)

    @property
    def access_token(self):
        self._check_appid_appsecret()
        # access_token = self.app.cache.get(self.prefix, self.token_key)
        access_token = self.r.get(self.prefix + self.token_key)
        if access_token:
            return access_token
        logging.debug('token expire, get token from server')
        self.grant_token()
        return self._WechatBasic__access_token

    def grant_token(self, override=True):
        """
        获取 Access Token
        详情请参考 http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        :param override: 是否在获取的同时覆盖已有 access_token (默认为True)
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        self._check_appid_appsecret()

        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self._WechatBasic__appid,
                "secret": self._WechatBasic__appsecret,
            }
        )
        access_token = response_json['access_token']
        expires_in = response_json['expires_in']
        expires_in = int(expires_in) / 2
        self.r.set(self.prefix + self.token_key, access_token)
        self.r.expire(self.prefix + self.token_key, expires_in)

        logging.debug('grant_token: {response_json}'.format(response_json=response_json))
        if override:
            self._WechatBasic__access_token = access_token
            self._WechatBasic__access_token_expires_at = expires_in
        return response_json

    def get_openid(self, code):
        r = requests.get(
            'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
                self.appid, self.appsecret, code))

        logging.debug('get access_token result: %s' % r.text)
        return r.json().get('openid')


class MyCachedWechatBasic(CachedWechatBasic):

    def init_app(self, app):
        self.app = app

        config = app.config
        self.token_key = config.get('WECHAT_ACCESS_TOKEN_KEY')
        self.reply_template = config.get('WECHAT_APP_REPLY_TEMPLATE')
        self.oauth2_url = config.get('WECHAT_OAUTH2_URL')

        self.token = config.get('WECHAT_APP_TOKEN')
        self.appid = config.get('WECHAT_APP_ID')
        self.appsecret = config.get('WECHAT_APP_SECRET')

        self._auth(self.token, self.appid, self.appsecret)
        logging.info('MY WECHAT TOKEN: %s' % self.get_access_token())