# -*- coding: UTF-8 -*-
# __author__ = xutao

from . import wechat_app
from . import wechat as my_wechat
from flask import current_app, request, render_template

from wechat_sdk.messages import *


@wechat_app.route("/index/", methods=['GET'])
def index():
    return render_template("index.html")


@wechat_app.route("/public", methods=['GET', 'POST'])
def call():
    current_app.logger.debug('Wechat call, request %s' % request)
    signature = request.args.get('signature')
    if not signature:
        return '{}'

    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    body_text = request.data
    current_app.logger.debug(body_text)
    if not body_text:
        current_app.logger.debug("It's change server settings")
        return echostr
    else:
        current_app.logger.debug(" start response")
        current_wechat = my_wechat

    return wechat_response(signature=signature, timestamp=timestamp, nonce=nonce, body_text=body_text,
                           wechat=current_wechat)


def wechat_response(signature, timestamp, nonce, body_text, wechat):
    current_app.logger.debug("start wechat response")

    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
        wechat.parse_data(body_text)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()

        response = None

        if isinstance(message, TextMessage):
            wechat_user = wechat.get_user_info(user_id=message.source)
            content = _text_message(message=message.content, wechat_user=wechat_user)
            if not content:
                return ""
            response = wechat.response_text(content=content)

        elif isinstance(message, EventMessage):  # 事件信息
            wechat_user = wechat.get_user_info(user_id=message.source)
            if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                pass
            elif message.type == 'unsubscribe':  # 取关
                pass
            elif message.type == 'scan':
                current_app.logger.debug("start scan")
                user_info = get_user_info_from_wechat(wechat_user)
                info = fomat_user(user_info)
                response = welcome_user(wechat=wechat, nickname=info[1], avatar_url=info[2])
            elif message.type == 'location':
                pass
            elif message.type == 'click':
                pass
            elif message.type == 'view':
                pass
            elif message.type == 'templatesendjobfinish':
                pass
        else:
            return ""  # 其它事件，暂时不处理
        current_app.logger.debug('Wechat call response %s' % response)
        return response

    else:
        current_app.logger.info(
            'check_signature fail!{signature} | {timestamp} | {nonce}'.format(signature=signature, timestamp=timestamp,
                                                                              nonce=nonce))


def _text_message(message, wechat_user):
    """
        返回文本信息
    :param message: 文本信息
    :param wechat_user: 用户
    :return:
    """
    user_info = get_user_info_from_wechat(wechat_user)
    return fomat_user(info=user_info, message=message)


def get_user_info_from_wechat(wechat_user):
    """
        获取微信用户详细信息
    :param wechat_user: 微信用户
    :return:
    """
    openid = wechat_user.get('openid')
    nickname = wechat_user.get('nickname').strip()  # 格式化下
    url = wechat_user.get('headimgurl')
    if url:
        avatar_url = url
    else:
        avatar_url = "http://data.ihaoyisheng.com/169258_avatar.jpeg"   # 默认给张图片

    sex_code = wechat_user.get("sex")
    if sex_code == 1:
        sex = u'男'
    elif sex_code == 0:
        sex = u'未知'
    else:
        sex = u'女'   # 1： 男, 2: 女
    province = wechat_user.get("province")
    city = wechat_user.get("city")
    country = wechat_user.get("country")

    return openid, nickname, avatar_url, sex, province, city, country


def fomat_user(info, message=u'关注信息自动回复'):
    """
        格式化用户信息
    :param info: 用户信息元祖
    :return:
    """
    return u"openid:%s; 微信名:%s; 头像:%s; 性别:%s; 省份:%s; 城市:%s; 国家:%s\n" \
           u"来自于 %s" % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], message)


def welcome_user(wechat, nickname, avatar_url):
    current_app.logger.debug("start welcome")
    welcome_title = [
        {
            'title': u'欢迎您:%s' % nickname,
            'picurl': u'%s' % avatar_url,
            'url': u'#',
        }
    ]

    response = wechat.response_news(welcome_title)
    return response