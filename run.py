# -*- coding: UTF-8 -*-
# __author__ = xutao

from wechat import wechat_app

if __name__ == "__main__":

    from os import environ
    wechat_app.run(host="127.0.0.1", port=environ.get("PORT", 8989), processes=2)
