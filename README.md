CodeNow教育直播平台部署文档
本工程须在ubuntu系统下运行，需安装Django，mysql，python2.x等。
将工程克隆到本地：

```
   git clone git@se.jisuanke.com:live-education/Group1.git
```

安装依赖：

```
   cd Group1
   pip install requirements.txt
```

建立数据库，在mysql下执行：

```
   create database live default character set utf8 collate utf8_unicode_ci;
```

在live/settings.py中：

```
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'live',
        'USER': 'root',
        'PASSWORD': 'vagrant'
      }
   }
```

   将PASSWORD改为自己数据库的密码
退出mysql，在Group1目录下执行

```
   ./manage.py makemigrations backend
   ./manage.py migrate
```

在Group1目录下,执行：

```
   cd frontend
   npm install
```

在Group1/frontend目录下，执行：

```
   npm run watch
```

在Group1/frontend目录下，执行：

```
   node index.js
```

在Group1目录下，执行：

```
   ./manage.py runserver 0:8000
```

在chrome浏览器下输入地址：

```
   localhost:8000
```

   即可正常使用。

