import traceback
import sqlite3, os, random, asyncio, requests, json, time, sys, re,uuid
from datetime import *
from config import domain,db_path
import random, randomstring
import platform,subprocess

os_type = platform.system()

#bot to program by whitehole


osnames = ""
name = ""
flag = ""
startFlag = False
info_me = {"expiredate":"","domain":"","name":"","resident_registration_number":"","address":"","date":"","region":"","picture":""}


def start_db():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    return con, cur

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

def make_expiretime(days):
    ServerTime = datetime.now()
    ExpireTime_STR = (ServerTime + timedelta(days=days)
                      ).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR


def isCreated(id):
    global startFlag

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
    user_info = cur.fetchone()
    con.close()
    if (user_info == None):
            return "Not register"
    else:
        startFlag = True
        name = input("[1/6] 이름을 적어주세요 예) 홍길동) > ")
        clear()
        num = input("[2/6] 주민등록번호를 적어주세요 예) 040101-3537921) > ")
        if len(num) != 14 or num[6] != "-":
            return "Invaild num"
        clear()
        address = input("[3/6] 주소를 입력 해 주세요.\n본인 집 주소 또는 위조민증을 사용하실 집 주소를 상세히 입력해주세요\n예) 경기도 고양시 일산동구 하늘마을1로 105, 306동 902호(중산동, 하늘마을) > ")
        clear()
        make = input("[4/6] 주민등록증 일자를 적어주세요.\n예) 2021.10.15\n\n점(.) 하나 까지 지켜주셔야합니다, 나이에 맞게 요령껏 만드세요! ( + 주민등록증을 언제 발급받았는지 표기 되는 부분이기 때문에 나이 맞게 잘 부탁드립니다) > ")
        clear()
        region = input("민증 발급 지역을 입력해주세요.\n예) 부산광역시 남구청장\n\n지역 적으실때는 광역시 또는 특별시는 OO구청장, 시 일때는 oo시장 입니다 부산광역시 남'구청장', 경기도 김포'시장' > ")
        clear()
        imgurl = input("증명사진 URL을 적어주세요 > ")
        if imgurl.startswith("https://"):
            try:
                query=randomstring.pick(20)
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                new_expiredate = make_expiretime(9999)
                cur.execute("UPDATE users SET expiredate = ? WHERE id == ?;",(new_expiredate, id))
                con.commit()
                cur.execute("UPDATE users SET query = ? WHERE id == ?;",(query, id))
                cur.execute("UPDATE users SET 이름 = ? WHERE id == ?;",(name, id))
                cur.execute("UPDATE users SET 주민등록번호 = ? WHERE id == ?;",(num, id))
                cur.execute("UPDATE users SET 집주소 = ? WHERE id == ?;",(address, id))
                cur.execute("UPDATE users SET 주민등록일자 = ? WHERE id == ?;",(make, id))
                cur.execute("UPDATE users SET 지역 = ? WHERE id == ?;",(region, id))
                cur.execute("UPDATE users SET 얼굴사진 = ? WHERE id == ?;",(str(imgurl), id))
                con.commit()
                con.close()
                return "success"
            except Exception as e:
                return "fail"
        else:
            return "imgurl startswith is not https"

def isFindid():
    osname = isCheck()
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE osname == ?;", (osname,))
    user_info = cur.fetchone()
    con.close()
    try:
        if user_info == None:
            return "Not Register"
        else:
            return user_info[0]
    except Exception as e:
        return input("알 수 없는 오류")


def isAboutMe(id):
    global info_me
    global domain
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
    user_info = cur.fetchone()
    con.close()
    try:
        if (user_info == None):
            return "Not Register"
        else:
            if str(user_info[0]) == str(id):
                if user_info[2] != None:
                    info_me["expiredate"] = user_info[2]
                    info_me["name"] = user_info[4]
                    info_me["resident_registration_number"] = user_info[5]
                    info_me["address"] = user_info[6]
                    info_me["date"] = user_info[7]
                    info_me["region"] = user_info[8]
                    if domain == '':
                        domain = "config.py에 도메인을 설정하지 않았습니다"
                    info_me["domain"] = f"{domain}/{user_info[3]}"
                    return "success"
            else:
                return "Invaild id"
    except Exception as e:
        return f"{e}"
   


def Register(id,osname):
    global flag
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE osname == ?;", (osname,))
    user_info = cur.fetchone()
    if user_info == None:
        cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?);", (id, None, None, None, None, None, None, None, None, None,osname))
        con.commit()
        con.close()
        return "success"
    else:
        flag = "already"
    con.close()

def clear():
    global name
    if os_type == "Windows":
        name = "Windows"
    if os_type == "Darwin":
        name = "Mac"

    if name == "Windows":
        return os.system("cls")
    if name == "Mac":
        return os.system("clear")
    
def isCheck():
    global osnames
    if os_type == "Windows":
        osnames = subprocess.check_output('hostname').strip().decode('utf-8')
    if os_type == "Darwin":
        osnames = subprocess.check_output(['scutil', '--get', 'ComputerName']).strip().decode('utf-8')
    if os_type == "Linux":
        osnames = subprocess.check_output('hostname').strip().decode('utf-8')

    return osnames

def main():
    while True:
        input_ = input("명령어를 입력 해 주세요(help - command list) > ")

        if input_ == "help":
            clear()
            print("""
            help - 도움말
            
            aboutme <ID> - 내정보
                        
            register - 가입 (고유 아이디 꼭 기억)
                        
            gen <ID> - 위조민증생성 시작

            find - 내 아이디 찾기
                        
            reload - 메뉴 리로딩

            exit - 프로그램 종료
            """)
            continue
        
        if input_ == "exit":
            break

        if input_ == "test":
            print(isCheck())

        elif input_ == "find":
            ID = isFindid()
            if ID == "Not Register":
                print("등록되지 않은 유저 입니다.\nregister 명령어로 등록 해 주세요.")
            else:
                print(f"회원님의 아이디는 {ID}입니다.")

        elif input_ == "reload":
            clear()
            continue

        elif input_.startswith("aboutme "):
            #clear()
            id = input_.split("aboutme ")[1]
            if id == "":
                print("aboutme <ID>")
            else:
                about_me = isAboutMe(id)
                if about_me == "Not Register":
                    print("가입이 안 되셨습니다.")
                elif about_me == "Invaild id":
                    print("아이디가 잘못 되셨습니다. 가입을 하시거나 아이디를 확인 해 주세요.")
                elif about_me == "success":
                    print(f"""
                    만기일 : {info_me["expiredate"]}

                    이름 : {info_me["name"]}
                    가상 주민등록번호 : {info_me["resident_registration_number"]}
                    가상 집주소 : {info_me["address"]}
                    가상 주민등록일자 : {info_me["date"]}
                    가상 지역 : {info_me["region"]}
                    사이트주소 : {info_me["domain"]}

                    https://github.com/WhiteHole00
                    """)
                else:
                    print(about_me)

        elif input_ == "register":
            clear()
            try:
                global name
                if os_type == "Windows":
                    name = subprocess.check_output('hostname').strip().decode('utf-8')
                if os_type == "Darwin":
                    name = subprocess.check_output(['scutil', '--get', 'ComputerName']).strip().decode('utf-8')
                if os_type == "Linux":
                    name = subprocess.check_output('hostname').strip().decode('utf-8')
                

                register_id = ''.join([str(random.randint(0, 9)) for _ in range(9)])
                regi = Register(register_id,name)
                global flag

                if regi == "success":
                    print(f"회원님의 아이디 : {register_id}")
                if flag == "already":
                    print("이미 가입 되어있습니다.")
                
            except Exception as e:
                print(e)
                print("알 수 없는 오류!")

        elif input_.startswith("gen "):
            global startFlag
            
            clear()
            ids = input_.split("gen ")[1]

            gen =  isCreated(ids)

            if gen == "Not register":
                print("가입을 먼저 해 주세요.")
            if startFlag == True:
                if gen == "Invaild num":
                    print("주민등록번호는 14자리(-포함) 입니다. 양식에 맞게 다시 적어주세요.")
                if gen == "success":
                    print("성공적으로 완성되었습니다.")
                if gen == "imgurl startswith is not https":
                    print("이미지 url을 적어주세요.")
            
        else:
            print("잘못된 명령어 입니다.")

        input("\n명령어 실행이 완료되었습니다. 계속하려면 엔터를 누르세요...")
        clear()


if __name__ == "__main__":
    main()
