from re import S
from flask import request, redirect, url_for, render_template, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from main.sent_mail import to_mail
import datetime
from models import User
import sqlite3
import pandas as pd
import hashlib


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
                print(user_ids[names.index(request.form["username"])])
                print(user_ids[names.index(request.form["username"])])
                session["user_id"] = user_ids[names.index(request.form["username"])]
                return redirect(url_for("show_entries"))
            else:
                flash("パスワードが異なります")
        else:
            flash("ユーザ名が異なります")


    return render_template("login.html")


#タスク用
@app.route("/taskm.html")
def show_entries_taskm():
    if (not session.get("logged_in")) or  (not session.get("username")) or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    else:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM Task_text', conn)

        cur.close()
        conn.close()

        # doneタスク読み込み
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        # dbをpandasで読み出す。
        df2 = pd.read_sql('SELECT * FROM daily_data', conn)
        cur.close()
        conn.close()
        user_ids2 = df2['user_id'].values.tolist()
        date2 = df2['date'].values.tolist()
        task_id2 = df2['task_id'].values.tolist()
        done_log = True
        if not(int(session["user_id"]) in user_ids2):
            done_log = False
        else:
            dt_now = datetime.datetime.now()
            if not(dt_now.strftime('%Y/%m/%d') in date2):
                done_log = False


        user_ids = df['user_id'].values.tolist()
        task_texts = df['task_text'].values.tolist()
        task_ids = df['task_id'].values.tolist()
        point_m = df['point_m'].values.tolist()
        point_d = df['point_d'].values.tolist()
        point_n = df['point_n'].values.tolist()
        ta_tasks = {}
        for x,y,z1,z2,z3,p in zip(task_texts,task_ids,point_m,point_d,point_n,user_ids):
            if int(p) == 0 or int(p) == int(session["user_id"]):
                if z1 != 0:
                    if not(done_log):
                        ta_tasks[y] = [x,0,[z1,z2,z3]]
                    else:
                        if y in task_id2:
                            df3 = df2[df2['user_id'] == session.get("user_id")]
                            done_done = df3[df3["date"] == dt_now.strftime('%Y/%m/%d')]
                            if int(y) in done_done['task_id'].values.tolist():
                                ta_tasks[y] = [x,1,[z1,z2,z3]]
                            else:
                                ta_tasks[y] = [x,0,[z1,z2,z3]]
                        else:
                            ta_tasks[y] = [x,0,[z1,z2,z3]]


        #today_data=[point_m[names.index(session.get("username"))], point_d[names.index(session.get("username"))], point_n[names.index(session.get("username"))]]
    return render_template("entries/task.html",user_id=session["user_id"],user_name=session["username"], tasks=ta_tasks,task_time=0)

@app.route("/taskw.html")
def show_entries_taskw():
    if (not session.get("logged_in")) or  (not session.get("username")) or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    else:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM Task_text', conn)

        cur.close()
        conn.close()

        # doneタスク読み込み
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        # dbをpandasで読み出す。
        df2 = pd.read_sql('SELECT * FROM daily_data', conn)
        cur.close()
        conn.close()
        user_ids2 = df2['user_id'].values.tolist()
        date2 = df2['date'].values.tolist()
        task_id2 = df2['task_id'].values.tolist()
        done_log = True
        if not(int(session["user_id"]) in user_ids2):
            done_log = False
        else:
            dt_now = datetime.datetime.now()
            if not(dt_now.strftime('%Y/%m/%d') in date2):
                done_log = False


        user_ids = df['user_id'].values.tolist()
        task_texts = df['task_text'].values.tolist()
        task_ids = df['task_id'].values.tolist()
        point_m = df['point_m'].values.tolist()
        point_d = df['point_d'].values.tolist()
        point_n = df['point_n'].values.tolist()
        ta_tasks = {}
        for x,y,z1,z2,z3,p in zip(task_texts,task_ids,point_m,point_d,point_n,user_ids):
            if int(p) == 0 or int(p) == int(session["user_id"]):
                if z2 != 0:
                    if not(done_log):
                        ta_tasks[y] = [x,0,[z1,z2,z3]]
                    else:
                        if y in task_id2:
                            df3 = df2[df2['user_id'] == session.get("user_id")]
                            done_done = df3[df3["date"] == dt_now.strftime('%Y/%m/%d')]
                            if int(y) in done_done['task_id'].values.tolist():
                                ta_tasks[y] = [x,1,[z1,z2,z3]]
                            else:
                                ta_tasks[y] = [x,0,[z1,z2,z3]]
                        else:
                            ta_tasks[y] = [x,0,[z1,z2,z3]]

        #today_data=[point_m[names.index(session.get("username"))], point_d[names.index(session.get("username"))], point_n[names.index(session.get("username"))]]
    return render_template("entries/task.html",user_id=session["user_id"],user_name=session["username"], tasks=ta_tasks,task_time=1)

@app.route("/taskn.html")
def show_entries_taskn():
    if (not session.get("logged_in")) or  (not session.get("username")) or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    else:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM Task_text', conn)

        cur.close()
        conn.close()

        # doneタスク読み込み
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        # dbをpandasで読み出す。
        df2 = pd.read_sql('SELECT * FROM daily_data', conn)
        cur.close()
        conn.close()
        user_ids2 = df2['user_id'].values.tolist()
        date2 = df2['date'].values.tolist()
        task_id2 = df2['task_id'].values.tolist()
        done_log = True
        if not(int(session["user_id"]) in user_ids2):
            done_log = False
        else:
            dt_now = datetime.datetime.now()
            if not(dt_now.strftime('%Y/%m/%d') in date2):
                done_log = False


        user_ids = df['user_id'].values.tolist()
        task_texts = df['task_text'].values.tolist()
        task_ids = df['task_id'].values.tolist()
        point_m = df['point_m'].values.tolist()
        point_d = df['point_d'].values.tolist()
        point_n = df['point_n'].values.tolist()
        ta_tasks = {}
        for x,y,z1,z2,z3,p in zip(task_texts,task_ids,point_m,point_d,point_n,user_ids):
            if int(p) == 0 or int(p) == int(session["user_id"]):
                if z3 != 0:
                    if not(done_log):
                        ta_tasks[y] = [x,0,[z1,z2,z3]]
                    else:
                        if y in task_id2:
                            df3 = df2[df2['user_id'] == session.get("user_id")]
                            done_done = df3[df3["date"] == dt_now.strftime('%Y/%m/%d')]
                            if int(y) in done_done['task_id'].values.tolist():
                                ta_tasks[y] = [x,1,[z1,z2,z3]]
                            else:
                                ta_tasks[y] = [x,0,[z1,z2,z3]]
                        else:
                            ta_tasks[y] = [x,0,[z1,z2,z3]]


        #today_data=[point_m[names.index(session.get("username"))], point_d[names.index(session.get("username"))], point_n[names.index(session.get("username"))]]
    return render_template("entries/task.html",user_id=session["user_id"],user_name=session["username"], tasks=ta_tasks,task_time=2)

# タスク追加用
@app.route("/addtask", methods=["GET", "POST"])
def addtask():
    if (not session.get("logged_in")) or  (not session.get("username"))or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            if request.form["newtask"] == "":
                flash("TASK内容を入力してください")
            else:
                if request.form["newpoint"] == "":
                    flash("重要度を入力してください")
                else:
                    conn = sqlite3.connect("test.db")
                    cur = conn.cursor()

                    # dbをpandasで読み出す。
                    df = pd.read_sql('SELECT * FROM Task_text', conn)

                    cur.close()
                    conn.close()

                    task_ids = df['task_id'].values.tolist()
                    new_task_id = max(task_ids)+1
                    newtask = request.form["newtask"]
                    newpoint_m = 0
                    newpoint_d = 0
                    newpoint_n = 0
                    if request.form["selecttime"] == "m":
                        newpoint_m = request.form["newpoint"]
                    elif request.form["selecttime"] == "d":
                        newpoint_d = request.form["newpoint"]
                    else:
                        newpoint_n = request.form["newpoint"]

                    #email = request.form["email"]

                    conn = sqlite3.connect("test.db")
                    cur = conn.cursor()

                    #cur.executemany("insert into users(user_id, name, password) values(int("+str(new_user_id)+"), '"+newusername+"', '"+newpassword+"');")
                    # SQLテンプレート
                    sql_insert_many = "INSERT INTO Task_text VALUES (?, ?, ?, ?, ?, ?, ?)"

                    # データの挿入
                    cur.execute(sql_insert_many, (int(new_task_id), session.get("user_id"), newtask, new_task_id, newpoint_m, newpoint_d, newpoint_n))
                    cur.close()
                    conn.commit()
                    conn.close()
                    flash("タスクを追加しました")
                    return render_template("entries/addtask.html")
        #users = session_1.query(User).all()
    return render_template("entries/addtask.html")

#グラフ用
@app.route("/graph.html")
def show_entries_graph():
    if (not session.get("logged_in")) or  (not session.get("username"))or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    else:
        session["subtra"] = 0
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM monthly_data', conn)

        cur.close()
        conn.close()
        df['user_id'] = df['user_id'].astype(int)
        user_ids = df['user_id'].values.tolist()
        # date = df['date'].values.tolist()
        # point_m = df['point_m'].values.tolist()
        # point_d = df['point_d'].values.tolist()
        # point_n = df['point_n'].values.tolist()


        if not(session["user_id"] in user_ids):
            datas = {}
            dt_now = datetime.datetime.now()
            for i in range(7):
                i_time = datetime.timedelta(days=i)
                datas[(dt_now -i_time).strftime('%Y/%m/%d')] = [0,0,0]
        else:
            user_df = df[df['user_id'] == session.get("user_id")]
            print(user_ids)
            date = user_df['date'].values.tolist()
            dt_now = datetime.datetime.now()
            datas = {}
            print(date)
            print((dt_now).strftime('%Y/%m/%d'))
            for i in range(7):
                i_time = datetime.timedelta(days=i)
                if not((dt_now -i_time).strftime('%Y/%m/%d') in date):
                    datas[(dt_now -i_time).strftime('%Y/%m/%d')] = ([0,0,0])
                else:
                    point = user_df[user_df["date"] == (dt_now -datetime.timedelta(days=i)).strftime('%Y/%m/%d')]
                    datas[(dt_now -i_time).strftime('%Y/%m/%d')] = ([str(int(point['point_m'].values[0])), str(int(point['point_d'].values[0])), str(int(point['point_n'].values[0]))])
    return render_template("entries/graph.html",da=datas)

#グラフ用　画面遷移
@app.route("/graph.html", methods=["POST"])
def graph_many():
        if (not session.get("logged_in")) or  (not session.get("username"))or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
            return redirect(url_for("login"))
        else:
            if not session.get("subtra"):
                subtra = int(request.form["subtra"]) * 7
            else:
                subtra = int(request.form["subtra"]) * 7 + int(session.get("subtra"))
            session["subtra"] = subtra
            conn = sqlite3.connect("test.db")
            cur = conn.cursor()

            # dbをpandasで読み出す。
            df = pd.read_sql('SELECT * FROM monthly_data', conn)

            cur.close()
            conn.close()
            df['user_id'] = df['user_id'].astype(int)

            user_ids = df['user_id'].values.tolist()



            if not(session.get("user_id") in user_ids):
                datas = {}
                dt_now = datetime.datetime.now()
                for i in range(7):
                    i_time = datetime.timedelta(days=i -subtra)
                    datas[(dt_now -i_time).strftime('%Y/%m/%d')] = [0,0,0]
            else:
                user_df = df[df['user_id'] == session.get("user_id")]
                date = user_df['date'].values.tolist()
                dt_now = datetime.datetime.now()
                datas = {}
                for i in range(7):
                    i_time = datetime.timedelta(days=i-subtra)
                    if not((dt_now -i_time).strftime('%Y/%m/%d') in date):
                        datas[(dt_now -i_time).strftime('%Y/%m/%d')] = ([0,0,0])
                    else:
                        point = user_df[user_df["date"] == (dt_now -datetime.timedelta(days=i-subtra)).strftime('%Y/%m/%d')]
                        datas[(dt_now -i_time).strftime('%Y/%m/%d')] = ([str(int(point['point_m'].values[0])), str(int(point['point_d'].values[0])), str(int(point['point_n'].values[0]))])
        return render_template("entries/graph.html",da=datas)

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
                hash_name = hashlib.md5(newusername.encode()).hexdigest()

                conn = sqlite3.connect("test.db")
                cur = conn.cursor()

                #cur.executemany("insert into users(user_id, name, password) values(int("+str(new_user_id)+"), '"+newusername+"', '"+newpassword+"');")
                # SQLテンプレート
                sql_insert_many = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)"

                # データの挿入
                cur.execute(sql_insert_many, (int(new_user_id), int(new_user_id), str(newusername), str(newpassword), email, str(hash_name)))
                cur.close()
                conn.commit()
                conn.close()
                session["logged_in"] = True # logged_inにTrueを代入
                session["username"] = newusername
                session["user_id"] = int(new_user_id)
                return redirect(url_for("show_entries"))
    #users = session_1.query(User).all()
    return render_template("signin.html")

@app.route("/task_done", methods=["GET", "POST"])
def task_done():
    if (not session.get("logged_in")) or  (not session.get("username"))or  (not session.get("user_id")): # ログインしてない場合ログイン画面に誘導
        return redirect(url_for("login"))
    get_task_id = request.form["task"]
    task_time = int(request.form["time"])
    print(task_time)
    #print("done" + task)
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    df = pd.read_sql('SELECT * FROM daily_data', conn)
    ids = df['id'].values.tolist()
    new_id = max(ids)+1
    
    cur.close()
    conn.close()
    
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    df = pd.read_sql('SELECT * FROM Task_text', conn)

    
   
    point_m = df['point_m'].values.tolist()
    point_d = df['point_d'].values.tolist()
    point_n = df['point_n'].values.tolist()
    task_id = df['task_id'].values.tolist()
    task_user_id = df['user_id'].values.tolist()

    full_point_m = 0
    full_point_d = 0
    full_point_n = 0
    for i in range(len(task_id)):
        if task_user_id[i] == 0 or task_user_id[i] == session["user_id"]:
            full_point_m += point_m[i]
            full_point_d += point_d[i]
            full_point_n += point_n[i]




    #print(get_task_id)
    get_point_m = 0
    get_point_d = 0
    get_point_n = 0
    if task_time == 0:
        get_point_m = point_m[task_id.index(int(get_task_id))]
    if task_time == 1:
        get_point_d = point_d[task_id.index(int(get_task_id))]
    else:
        get_point_n = point_n[task_id.index(int(get_task_id))]

    
    


    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y/%m/%d')
    print(dt_now)

    #cur.executemany("insert into users(user_id, name, password) values(int("+str(new_user_id)+"), '"+newusername+"', '"+newpassword+"');")
    # SQLテンプレート
    sql_insert_many = "INSERT INTO daily_data VALUES (?, ?, ?, ?, ?, ?, ?)"

    # データの挿入
    #print((int(new_id), session["user_id"], get_task_id, get_point_m, get_point_d, get_point_n, str(dt_now)))
    cur.execute(sql_insert_many, (int(new_id), session.get("user_id"), get_task_id, get_point_m, get_point_d, get_point_n, str(dt_now)))
    
    df = pd.read_sql('SELECT * FROM daily_data', conn)

    point_m = df['point_m'].values.tolist()
    point_d = df['point_d'].values.tolist()
    point_n = df['point_n'].values.tolist()
    task_user_id = df['user_id'].values.tolist()

    have_point_m = 0
    have_point_d = 0
    have_point_n = 0
    for i in range(len(point_m)):
        if task_user_id[i] == 0 or task_user_id[i] == session["user_id"]:
            have_point_m += point_m[i]
            have_point_d += point_d[i]
            have_point_n += point_n[i]


    
    
    cur.close()
    conn.commit()
    conn.close()

    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    df = pd.read_sql('SELECT * FROM monthly_data', conn)
    ids = df['id'].values.tolist()
    user_id = df['user_id'].values.tolist()
    date = df['date'].values.tolist()
    new_id = max(ids)+1
    
    cur.close()
    conn.close()

    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    point_per_m = have_point_m / full_point_m * 100
    point_per_d = have_point_d / full_point_d * 100
    point_per_n = have_point_n / full_point_n * 100

    #cur.executemany("insert into users(user_id, name, password) values(int("+str(new_user_id)+"), '"+newusername+"', '"+newpassword+"');")
    # SQLテンプレート
    sql_insert_many = "INSERT INTO monthly_data VALUES (?, ?, ?, ?, ?, ?)"

    # データの挿入
    jadge = 0
    

    for i in range(len(ids)):
        if user_id[i] == session["user_id"] and date[i] == dt_now:
            jadge += 1
            cur.execute("update monthly_data set point_m=?, point_d=?, point_n=? where id=?",(point_per_m, point_per_d, point_per_n, i+1))

    if jadge == 0:
        cur.execute(sql_insert_many, (int(new_id), session.get("user_id"), point_per_m, point_per_d, point_per_n, str(dt_now)))
    
    cur.close()
    conn.commit()
    conn.close()




    if task_time == 0:
        return redirect(url_for("show_entries_taskm"))
    elif task_time == 1:
        return redirect(url_for("show_entries_taskw"))
    elif task_time == 2:
        return redirect(url_for("show_entries_taskn"))
    else:
        print("===== task_time error ======")
        return redirect(url_for("show_entries_taskm"))

### パスワードの変更
# メールとユーザ名を入力、メールの送信
@app.route("/enteremail", methods=["GET", "POST"])
def enteremail():
    if request.method == "POST":
        session["reset_username"] = str(request.form["reset_username"])
        hash_name = hashlib.md5(session["reset_username"].encode()).hexdigest()
        session["email"] = str(request.form["email"])
        to_mail(session["reset_username"], session["email"])

        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        # dbをpandasで読み出す。
        df = pd.read_sql("SELECT hash_name, email FROM users WHERE hash_name='{}'".format(hash_name), conn)
        cur.close()
        conn.close()

        if len(df.values.tolist()) != 1:
            flash("登録されているユーザ名とメールアドレスが一致しません")
        else:
            db_hash_name = df.values.tolist()[0][0]
            db_email = df.values.tolist()[0][1]
            
            if (hash_name==db_hash_name) and (session["email"]==db_email):
                to_mail(session["reset_username"], session["email"])
                return redirect(url_for("confirm"))
            # elif (hash_name!=db_hash_name) and (session["email"]==db_email):
            #     flash("登録されているユーザ名が一致しません")
            # elif (hash_name==db_hash_name) and (session["email"]!=db_email):
            #     flash("登録されているメールアドレスが一致しません")
            else:
                flash("登録されているユーザ名とメールアドレスが一致しません")
    return render_template("enteremail.html")

# メールの送信確認
@app.route("/confirm")
def confirm():
    flash("{}にメールを送りました。メールを確認してパスワードリセットを完了させてください。".format(session["email"], category="alert alert-info"))
    return render_template("confirm.html")

# パスワードの変更
@app.route("/passwordchange", methods=["GET", "POST"])
def passwordchange():
    if request.method == "POST":
        if request.form["pword"] == request.form["pword_again"]:
            reset_username = str(session["reset_username"])
            pword = str(request.form["pword"])

            conn = sqlite3.connect("test.db")
            cur = conn.cursor()
            sql_update = "UPDATE users SET password=? WHERE hash_name=?"
            cur.execute(sql_update, (pword, reset_username))
            cur.close()
            conn.commit()
            conn.close()

            flash("パスワードを変更しました")
            return redirect(url_for("login"))
        else:
            flash("同じパスワードを入力して下さい")
            return render_template("passwordchange.html")
    else:
        session["reset_username"] = request.args.get("reset_username")
        flash("新しいパスワードを入力してください")
        return render_template("passwordchange.html")