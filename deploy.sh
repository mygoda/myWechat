#!/usr/bin/env bash

source env/bin/activate
git pull
pip install -r requirements.txt -q -i http://pypi.douban.com/simple

supervisorctl update
supervisorctl restart wechat