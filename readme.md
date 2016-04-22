**一、DEV配置**

`cd aCloud`

`virtualenv venv`

`venv\Scripts\activate`

`pip install -r requirement.txt`

`venv\Scripts\deactivate`

**二、第三方库说明**

`1、服务器端发送Http请求 requests`

`2、加密解密 rsa`

`3、验证码识别 pytesseract、PIL(Pillow)、tesseract-ocr`

`tesseract路径配置：`

` CHANGE THIS IF TESSERACT IS NOT IN YOUR PATH, OR IS NAMED DIFFERENTLY`

`tesseract_cmd = 'tesseract'`

`4、sqlacodegen用法`

`sqlacodegen postgresql:///some_local_db`

`sqlacodegen mysql://user:password@localhost/dbname`

`sqlacodegen sqlite:///database.db`

`sqlacodegen --help`

`如：venv\Scripts\sqlacodegen mysql://root:hcy123456@127.0.0.1/ecshop > dbmodel.py`

**三、部署**

`Nginx configuration`

`server {`

`    listen 80;`

`    server_name you-domain;`

`    location / {`

`      fastcgi_pass  127.0.0.1:7777;`

`      root /var/path-to-chili/;`

`      fastcgi_param REQUEST_URI       $request_uri;`

`      fastcgi_param REQUEST_METHOD    $request_method;`

`      fastcgi_param QUERY_STRING      $query_string;`

`      fastcgi_param CONTENT_TYPE      $content_type;`

`      fastcgi_param CONTENT_LENGTH    $content_length;`

`      fastcgi_param SERVER_ADDR       $server_addr;`

`      fastcgi_param SERVER_PORT       $server_port;`

`      fastcgi_param SERVER_NAME       $server_name;`

`      fastcgi_param SERVER_PROTOCOL   $server_protocol;`

`      fastcgi_param PATH_INFO         $fastcgi_script_name;`

`      fastcgi_param REMOTE_ADDR       $remote_addr;`

`      fastcgi_param REMOTE_PORT       $remote_port;`

`      fastcgi_pass_header Authorization;`

`      fastcgi_intercept_errors off;`

`    }`

`}`
