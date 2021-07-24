from flask import request, redirect, url_for, render_template, flash, session
from main import app

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
        if request.form["username"] != app.config["USERNAME"]:
            flash("ユーザ名が異なります")
        elif request.form["password"] != app.config["PASSWORD"]:
            flash("パスワードが異なります")
        # ログイン完了後メイン画面に遷移
        else:
            session["logged_in"] = True # logged_inにTrueを代入
            flash("ログインしました")
            return redirect(url_for("show_entries"))

    return render_template("login.html")

# ログアウト画面での挙動
@app.route("/logout")
def logout():
    session.pop("logged_in", None) # logged_inを空にする
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))