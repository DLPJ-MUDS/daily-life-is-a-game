from flask import request, redirect, url_for, render_template, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
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

engine = create_engine('sqlite:///test.db')
session_1 = sessionmaker(bind=engine)()

# メイン画面での挙動
@app.route("/")
def show_entries():
    if not session.get("logged_in"): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/index.html")

# ログイン画面での挙動
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        #users = session_1.query(User).all()
        if request.form["username"] in names:
            if request.form["password"] == passwords[names.index(request.form["username"])]:
                session["logged_in"] = True # logged_inにTrueを代入
                flash("ログインしました")
                return redirect(url_for("show_entries"))
            else:
                flash("パスワードが異なります")
        else:
            flash("ユーザ名が異なります")
        
            

    return render_template("login.html")

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