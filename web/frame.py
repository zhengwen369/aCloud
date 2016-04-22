#  -*- coding: utf-8 -*-
from flask import Flask
from respository.dbmodel import db

app = Flask(__name__)
app.config.from_object("config")
db.app = app
db.init_app(app)
