# -*- coding: UTF-8 -*-
# __author__ = xutao

from wechat import wechat_app

if __name__ == "__main__":

    wechat_app.debug = True
    wechat_app.run(host="0.0.0.0", port=5001, processes=2)
