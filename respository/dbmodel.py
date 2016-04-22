# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Text, text
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model
metadata = db.metadata


class EcsArticle(Base):
    __tablename__ = 'ecs_article'

    article_id = Column(Integer, primary_key=True)
    cat_id = Column(SmallInteger, nullable=False, index=True, server_default=text("'0'"))
    title = Column(String(150), nullable=False, server_default=text("''"))
    content = Column(String, nullable=False)
    author = Column(String(30), nullable=False, server_default=text("''"))
    author_email = Column(String(60), nullable=False, server_default=text("''"))
    keywords = Column(String(255), nullable=False, server_default=text("''"))
    article_type = Column(Integer, nullable=False, server_default=text("'2'"))
    is_open = Column(Integer, nullable=False, server_default=text("'1'"))
    add_time = Column(Integer, nullable=False, server_default=text("'0'"))
    file_url = Column(String(255), nullable=False, server_default=text("''"))
    open_type = Column(Integer, nullable=False, server_default=text("'0'"))
    link = Column(String(255), nullable=False, server_default=text("''"))
    description = Column(String(255))
