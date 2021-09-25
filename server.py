import os
import sqlite3
from flask import g
from flask import Flask
from flask import render_template

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "dev.db")


def connect_db():
    return sqlite3.connect(DATABASE)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """
    查询db
    :param query:
    :param args:
    :param one:
    :return:
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/top")
def move_top():
    return "<p>250经典电影</p>"


@app.route("/movie")
def movie_page():
    """
    电影页面
    :return:
    """
    movie_list = query_db('select * from movie')
    # for movie in movie_list:
    #     print("db-data\n", type(movie), movie)
    return render_template("hello.html", moves=movie_list)
