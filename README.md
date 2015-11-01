### 简易版本微信公众帐号
####  flask + redis + gunicorn + supervisor + wechat_sdk

### supervisor配置
	```[program:wechat]
	directory=/home/xutao/myWechat
	command=/opt/lambda/env/bin/gunicorn --workers=4 -b 127.0.0.1:8989 	wechat:wechat_app --log-level=debug
	autostart=true
	autorestart=true
	redirect_stderr=true
	stdout_logfile=/var/log/testwechat.log
	exitcodes=1```
	
	
### nginx配置

	
	```
	upstream wechat {
        server 127.0.0.1:8989;
	}
	server {

        listen 80;
        server_name app.mingyinet.com;
        location /{
                proxy_pass http://wechat;
        }

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
	}```
	

### 测试公众帐号二维码

![测试帐号](http://data.ihaoyisheng.com/d93ac5208955af98f60c66a3419146ed.png)


### 思路

1. 首先要让微信知道我们的公众帐号的服务器在哪里，配置好服务器。
2. 相关代码的架构，我这里使用了python wechat sdk 不再重复造轮子.
3. 获得用户授权的话，需要我们配置授权回调页面域名，不然我们是无法获取用户信息的，这是一个需要注意的
4. 往后就是一般的网页后台开发过程，因为使用了wechat python sdk 节省了大量工作