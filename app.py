from ast import dump
from crypt import methods
from encodings import utf_8
import hashlib
import json
from os import curdir
from sqlite3 import Cursor
from tabnanny import check
from itsdangerous import NoneAlgorithm
import mysql.connector
from flask import Flask, jsonify, redirect, request, render_template, url_for

app = Flask(__name__)


dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="gg04236@@",
    database="SNU"
)


# pw 검증
# 사용자 입력(request body)
# {
#   "name":,
#   "pw":
# }
def checking_pw(name):
    cursor = dataBase.cursor()

    sql = "SELECT pw from students WHERE name = %s"
    val = [name]

    cursor.execute(sql, val)

    result = cursor.fetchone()
    (data,)=result

    body = request.get_json()
    hashedPW = hashlib.md5(bytes(body["pw"]+"jiwoo", 'utf_8')).hexdigest()

    if data == hashedPW:
        return True
    else:
        return False


# name 존재여부 검증
def isnameExist(name):
    cursor = dataBase.cursor()

    sql = ("SELECT EXISTS(SELECT * FROM students where name = %s)")
    val = [name]

    cursor.execute(sql, val)

    result = cursor.fetchone()
    (data,)= result

    if data >= 1:
        return True
    else:
        return False

# print(isnameExist('jiwoo'))


# json으로 데이터 전달
# jsonify_02 -> [["{}""], ["{}"], ["{}""]] 이런식으로 나오는데 header에 content-type은 json이라고 되어있음.
# def returnJson(name):
#   cursor = dataBase.cursor()
#   sql = "SELECT JSON_OBJECT ('name', name, 'age', age, 'sex', sex, 'email', email, 'code', code, 'nickname', nickname, 'bio', bio) FROM students WHERE name = %s"
#   val = [name]
#   cursor.execute(sql, val)

#   result = cursor.fetchall()
#   for row in cursor:
#     result.append(row)

#   return jsonify(result)

# jsonify_03
def returnJson(name):
    cursor = dataBase.cursor()
    sql = "SELECT JSON_OBJECT ('name', name, 'age', age, 'sex', sex, 'email', email, 'code', code, 'nickname', nickname, 'bio', bio) FROM students WHERE name = %s"
    val = [name]
    cursor.execute(sql, val)
    result = cursor.fetchone()

    (data,) = result

    return jsonify(json.loads(data))


@app.route("/", methods=["GET", "POST"])
def signupPage():
    if request.method == "POST":
        return redirect(url_for('testpost'))
    return render_template('signup.html')


# CREATE
# 사용자 입력(request body)
# {
# 	"name": ,
# 	"age": ,
# 	"sex": ,
# 	"email": ,
# 	"pw":
# }
@app.route("/student", methods=["POST"])
def add_student():
    body = request.get_json()
    code = hashlib.md5(bytes(body["email"], 'utf-8')).hexdigest()
    pw = hashlib.md5(bytes(body["pw"]+"jiwoo", 'utf_8')).hexdigest()

    sql = "INSERT INTO students (name, age, sex, email, pw, code) VALUES(%s, %s, %s, %s, %s, %s)"
    val = (body["name"], body["age"], body["sex"], body["email"], pw, code)

    cursor = dataBase.cursor()

    cursor.execute(sql, val)
    dataBase.commit()

    # jsonify_01
    # json 오기는 하나, 개선필요 -> 1차 개선 완료(아래 jsonify_02)
    # sql = "SELECT JSON_OBJECT ('name', %s, 'age', %s, 'sex', %s, 'email', %s, 'code', %s)"
    # val = [result[0][0], result[0][1], result[0][2], result[0][3], result[0][5]]
    # cursor.execute(sql, val)
    # result = cursor.fetchall()
    # for row in cursor:
    #   result.append(row)
    # return jsonify(result[0])

    # jsonify_02 -> returnJson func
    result = returnJson(body["name"])

    return result


# html-flask-mysql
@app.route("/test", methods=["POST", "GET"])
# @app.route("/test")
def testpost():
    if request.method == "POST":
        # print(request.form.get('new_name', False))
        print(request.form['new_name'])
        print(request.form['new_age'])
        print(request.form['new_email'])
        print(request.form['new_sex'])
        print(request.form['new_pw'])

        
        name_value = request.form['new_name']
        age_value = request.form['new_age']
        sex_value = request.form['new_sex']
        email_value = request.form['new_email']
        pw_value = request.form['new_pw']
        

        code = hashlib.md5(bytes(email_value, 'utf-8')).hexdigest()
        pw = hashlib.md5(bytes(pw_value+"jiwoo", 'utf_8')).hexdigest()

        cursor = dataBase.cursor()
        sql = "INSERT INTO students (name, age, sex, email, pw, code) VALUES(%s, %s, %s, %s, %s, %s)" % (name_value, age_value, sex_value, email_value, pw, code)

        cursor.execute(sql)
        dataBase.commit()

        # sql = "SELECT * from students WHERE name = %s" % (name_value)
        # cursor = dataBase.cursor()
        # result = cursor.execute(sql)

        # return result
        return render_template('signup.html')
    else: 
        return "X"

        # result = returnJson(name_value)

        # return result



# READ
# 전체 학생 조회
@app.route("/student", methods=["GET"])
def student():
    cursor = dataBase.cursor()

    query = "SELECT JSON_OBJECT ('name', name, 'age', age, 'sex', sex, 'email', email, 'code', code, 'nickname', nickname, 'bio', bio) FROM students"
    cursor.execute(query)

    result = cursor.fetchall()
    for row in cursor:
        result.append(row)
    print(result)

    return jsonify(result)


# 학생 이름으로 조회
@app.route("/student/<name>", methods=["GET"])
def get_student_by_name(name):
    if isnameExist(name):
        result = returnJson(name)
        return result

    else:
        return "Wrong Name", 400


# UPDATE
# 이름, pw입력 (pw는 json 형태로 받기)
# 사용자 입력(request body)
# {
# 	"name": ,
#   "nickname": ,
#   "bio": ,
# 	"pw":
# }
@app.route("/student/<name>", methods=["PUT"])
def update_student_by_name(name):
    if isnameExist(name): 
        body = request.get_json()
        cursor = dataBase.cursor()
        
        if checking_pw(name):
            sql = "UPDATE students SET nickname = %s, bio = %s WHERE name = %s"
            val = (body["nickname"], body["bio"], body["name"])
            cursor.execute(sql, val)
            dataBase.commit()

            result = returnJson(name)
            return result

        else:
            return "Wrong PW", 400

    else:
        return "Wrong Name", 400


# DELETE
# 이름, pw입력 (pw는 json형태로 받기)
# 사용자 입력(request body)
# {
# 	"name": ,
# 	"pw":
# }
@app.route("/student/<name>", methods=["DELETE"])
def delete_student_by_name(name):
    if isnameExist(name):
        cursor = dataBase.cursor()
        if checking_pw(name):
            sql = "DELETE FROM students WHERE name = (%s)"
            val = [name]
            cursor.execute(sql, val)

            dataBase.commit()

            return "DELETE!"

        else:
            return "Wrong PW", 400

    else:
        return "Wrong Name", 400

# dataBase.close()
