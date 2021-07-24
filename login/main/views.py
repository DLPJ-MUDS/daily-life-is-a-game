from flask import request, redirect, url_for, render_template, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
import datetime
from models import User
import sqlite3
import pandas as pd


dt_now = datetime.datetime.now()



engine = create_engine('sqlite:///test.db')
session_1 = sessionmaker(bind=engine)()

# メイン画面での挙動
@app.route("/")
def show_entries():
    if (not session.get("logged_in")) or (not session.get("username")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/user.html",user_name=session["username"])

# ログイン画面での挙動
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        #users = session_1.query(User).all()
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM users', conn)

        cur.close()
        conn.close()

        user_ids = df['user_id'].values.tolist()
        names = df['name'].values.tolist()
        passwords = df['password'].values.tolist()
        if request.form["username"] in names:
            if request.form["password"] == passwords[names.index(request.form["username"])]:
                session["logged_in"] = True # logged_inにTrueを代入
                session["username"] = request.form["username"]
                session["user_id"] = user_ids[names.index(request.form["username"])]
                return redirect(url_for("show_entries"))
            else:
                flash("パスワードが異なります")
        else:
            flash("ユーザ名が異なります")


    return render_template("login.html")


#タスク用
@app.route("/task.html")
def show_entries_task():
    if (not session.get("logged_in")) or  (not session.get("username")) or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/task.html",user_id=session["userid"],user_name=session["username"])

#グラフ用
@app.route("/graph.html")
def show_entries_graph():
    if (not session.get("logged_in")) or  (not session.get("username"))or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    else:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM monthly_data', conn)

        cur.close()
        conn.close()

        user_ids = df['user_id'].values.tolist()
        date = df['date'].values.tolist()
        point_m = df['point_m'].values.tolist()
        point_d = df['point_d'].values.tolist()
        point_n = df['point_n'].values.tolist()
        print(user_ids)

        if not(session.get("user_id") in user_ids):
            today_data = [0,0,0]
        else:
            today_data=[point_m[user_ids.index(session.get("user_id"))], point_d[user_ids.index(session.get("user_id"))], point_n[user_ids.index(session.get("user_id"))]]
    return render_template("entries/graph.html",now_time=dt_now.strftime('%Y/%m/%d'),today_data=today_data)

#ユーザー画面用
@app.route("/user.html")
def show_entries_user():
    if (not session.get("logged_in")) or  (not session.get("username"))or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/user.html",user_name=session["username"])

# ログアウト画面での挙動
@app.route("/logout")
def logout():
    session.pop("logged_in", None) # logged_inを空にする
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))

# サインイン画面での挙動
@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = None
    if request.method == "POST":
        if request.form["newusername"] == "":
            flash("新しいユーザネームを入力してください")
        else:
            if request.form["newpassword"] == "":
                flash("新しいパスワードを入力してください")
            else:
                conn = sqlite3.connect("test.db")
                cur = conn.cursor()

                # dbをpandasで読み出す。
                df = pd.read_sql('SELECT * FROM users', conn)

                cur.close()
                conn.close()

                user_ids = df['user_id'].values.tolist()
                new_user_id = max(user_ids)+1
                newusername = request.form["newusername"]
                newpassword = request.form["newpassword"]
                email = request.form["email"]

                conn = sqlite3.connect("test.db")
                cur = conn.cursor()

                #cur.executemany("insert into users(user_id, name, password) values(int("+str(new_user_id)+"), '"+newusername+"', '"+newpassword+"');")
                # SQLテンプレート
                sql_insert_many = "INSERT INTO users VALUES (?, ?, ?, ?, ?)"

                # データの挿入
                cur.execute(sql_insert_many, (int(new_user_id), int(new_user_id), str(newusername), str(newpassword), email))
                cur.close()
                conn.commit()
                conn.close()
                session["logged_in"] = True # logged_inにTrueを代入
                session["username"] = newusername
                session["user_id"] = user_ids
                return redirect(url_for("show_entries"))
    #users = session_1.query(User).all()
    return render_template("signin.html")

@app.route("/task_done", methods=["GET", "POST"])
def task_done():
    session.pop("logged_in", None) # logged_inを空にする
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))

