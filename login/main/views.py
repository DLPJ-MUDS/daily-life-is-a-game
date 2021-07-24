from flask import request, redirect, url_for, render_template, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
import datetime
from models import User
import sqlite3
import pandas as pd



conn = sqlite3.connect("test.db")
cur = conn.cursor()

# dbをpandasで読み出す。
df = pd.read_sql('SELECT * FROM users', conn)

cur.close()
conn.close()

names = df['name'].values.tolist()
passwords = df['password'].values.tolist()
dt_now = datetime.datetime.now()


engine = create_engine('sqlite:///test.db')
session_1 = sessionmaker(bind=engine)()

# メイン画面での挙動
@app.route("/")
def show_entries():
    if (not session.get("logged_in")) or (not session.get("userid")) or (not session.get("username")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/user.html",user_name=session["username"],user_id=session["userid"])

# ログイン画面での挙動
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        #users = session_1.query(User).all()
        if request.form["username"] in names:
            if request.form["password"] == passwords[names.index(request.form["username"])]:
                session["logged_in"] = True # logged_inにTrueを代入
                session["username"] = request.form["username"]
                session["userid"] = "dokoka kara mottekuru"
                return redirect(url_for("show_entries"))
            else:
                flash("パスワードが異なります")
        else:
            flash("ユーザ名が異なります")
        
            

    return render_template("login.html")


#タスク用
@app.route("/task.html")
def show_entries_task():
    if (not session.get("logged_in")) or (not session.get("userid")) or (not session.get("username")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/task.html",user_id=session["userid"],user_name=session["username"])

#グラフ用
@app.route("/graph.html")
def show_entries_graph():
    if (not session.get("logged_in")) or (not session.get("userid")) or (not session.get("username")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/graph.html",now_time=dt_now.strftime('%Y/%m/%d'),today_data=[50,20,30])

#ユーザー画面用
@app.route("/user.html")
def show_entries_user():
    if (not session.get("logged_in")) or (not session.get("userid")) or (not session.get("username")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/user.html",user_id=session["userid"],user_name=session["username"])

# ログアウト画面での挙動
@app.route("/logout")
def logout():
    session.pop("logged_in", None) # logged_inを空にする
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))

# サインイン画面での挙動
@app.route("/signin", methods=["GET", "POST"])
def signin():
    #users = session_1.query(User).all()
    return render_template("signin.html", users=users)
