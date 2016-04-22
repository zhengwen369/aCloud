from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import *


db = SQLAlchemy()
Base = db.Model
metadata = db.metadata
