import os


# 设置中文
LANGUAGE_CODE = 'zh-hans'

# 设置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vul_server_py',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': os.getenv('VULN_SERVER_DB_HOST', "localhost"),
        'PORT': 3306,
    }
}