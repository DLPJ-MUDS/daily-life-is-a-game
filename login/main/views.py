from flask import request, redirect, url_for, render_template, flash, session
from main import app
import datetime



dt_now = datetime.datetime.now()

# メイン画面での挙動
@app.route("/")
def show_entries():
    if (not session.get("logged_in")) or (not session.get("userid")) or (not session.get("username")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    return render_template("entries/user.html",user_id=session["userid"],user_name=session["username"])

# ログイン画面での挙動
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["userid"] != app.config["USERNAME"]:
            flash("ユーザ名が異なります")
        elif request.form["password"] != app.config["PASSWORD"]:
            flash("パスワードが異なります")
        # ログイン完了後メイン画面に遷移
        else:
            session["logged_in"] = True # logged_inにTrueを代入
            session["userid"] = request.form["userid"]
            session["username"] = "dokoka kara mottekuru"
            return redirect(url_for("show_entries"))

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
    return render_template("entries/graph.html",now_time=dt_now.strftime('%Y/%m/%d'))

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
    return redirect(url_for("show_entries"))