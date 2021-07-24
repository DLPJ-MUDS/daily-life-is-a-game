import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

def to_mail(username, email):
    sendAddress = "s2022055@stu.musashino-u.ac.jp"
    password = "wlfxhlgmcybxkwsp"

    subject = "daily life is a game パスワードリセット"
    bodyText = """daily life is a gameのパスワードリセットを行います。リセットを行う際には下のURLを押して、手続きを進めて下さい。
http://localhost:5000/passwordchange?reset_username=""" + username
    fromAddress = "s2022055@stu.musashino-u.ac.jp"
    toAddress = str(email)

    # SMTPサーバに接続
    smtpobj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpobj.starttls()
    smtpobj.login(sendAddress, password)

    # メール作成
    msg = MIMEText(bodyText)
    msg["Subject"] = subject
    msg["From"] = fromAddress
    msg["To"] = toAddress
    msg["Date"] = formatdate()

    # 作成したメールを送信
    smtpobj.send_message(msg)
    smtpobj.close()