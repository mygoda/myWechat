# -*- coding: UTF-8 -*-
# __author__ = xutao
import requests

from qiniu import put_data
from wechat import wechat, q_token
from setting.setting import Config


def upload_img_by_wechat_media_id(media_id, user_id, response=None):
    if not response:
        response = wechat.download_media(media_id)
    filename = '%s_%s' % (user_id, media_id)
    url = upload_img(stream=response.content, filename=filename)
    return url, filename


def upload_img(stream, filename):
    put_data(up_token=q_token, key=filename, data=stream)
    return '%s/%s' % (Config.QINIU_BUCKET_DOMAIN, filename)


def upload_img_by_url(url, filename):
    r = requests.get(url=url, stream=True)
    return upload_img(stream=r.content, filename=filename)