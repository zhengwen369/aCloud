# -*- coding: utf-8 -*-

# Flask
DEBUG = True

# Flask-SQLAlchemy config
_SQL_PARAMS = {
    'passwd': 'hcy123456',
    'host': '127.0.0.1',
    'db': 'ecshop',
    'port': 3306,
    'user': 'root',
    }

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s" % (_SQL_PARAMS['user'], _SQL_PARAMS['passwd'], _SQL_PARAMS['host'], _SQL_PARAMS['port'], _SQL_PARAMS['db'])
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Flask-WTF config
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# temp
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]