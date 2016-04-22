#  -*- coding: utf-8 -*-
from flask import render_template
from web.frame import app
from respository.dbmodel import db, EcsArticle


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # make user
    posts = [  # make array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)


@app.route('/hello')
def hello_world():
    app.logger.log(1, "log test")
    # title = EcsArticle.query.filter(EcsArticle.title == "测试").first().content
    art = EcsArticle()
    art.title = "测试"
    art.content = "测试内容"
    # db.session.add(art)
    # db.session.commit()
    title = db.session.query(EcsArticle).filter(EcsArticle.title == "测试").first().content
    return 'Hello World!' + title


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

