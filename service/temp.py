#  -*- coding: utf-8 -*-
from flask import Flask
from respository.dbmodel import db, EcsArticle

app = Flask(__name__)
app.config.from_object("config")
db.app = app
db.init_app(app)

print db.session.query(EcsArticle).filter(EcsArticle.title == "测试").first().content