from flask import Flask, render_template, request, redirect, url_for, session, abort
import sqlite3
import datetime
from config import db_path
app = Flask(__name__)

def get_expiretime(time):
    ServerTime = datetime.now()
    ExpireTime = datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        how_long = (ExpireTime - ServerTime)
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        return str(round(days)) + "일 " + str(round(hours)) + "시간 " + str(round(minutes)) + "분"
    else:
        return False

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True

@app.route('/<code>')
def index(code):

    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE query = ?;", (code,))
        user_info = cur.fetchone()
        con.close()
    except:
        print("error")
        return render_template("error.html", title="접속 실패", dese="존재하지 않는 주소입니다.")
    print(user_info[2])
    if (is_expired(user_info[2])):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("UPDATE users SET query = ? WHERE id == ?;", (None, user_info[0]))
        con.commit()
        con.close()
        return render_template("error.html", title="접속 실패", dese="라이센스 유효기간이 만료되었습니다.")
    tmp=user_info[5].split("-")[0]
    date=f"{tmp[0:2]}.{tmp[2:4]}.{tmp[4:6]}"
    return render_template("sex.html", name = user_info[4],num = user_info[5],date =date,juso =user_info[6],make =user_info[7],jiname = user_info[8],imgurl = user_info[9])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
