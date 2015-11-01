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

	