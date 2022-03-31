from encodings import utf_8
import hashlib
import json
from os import curdir
from sqlite3 import Cursor
from itsdangerous import NoneAlgorithm
import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def WELCOME():
    return "<p>WELCOME! SNU DB</p>"


dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="gg04236@@",
  database ="SNU"
)


# pw 검증
# 사용자 입력(request body)
# {
#   "name":,
#   "pw":
# }
def checking_pw(name):
  cursor = dataBase.cursor()

  sql = "SELECT pw from student WHERE name = %s"
  val = [name]

  cursor.execute(sql, val)

  result = cursor.fetchall()
  for name in cursor:
    result.append(name)
  
  # print(result[0][0])

  body = request.get_json()
  hashedPW = hashlib.md5(bytes(body["pw"]+"jiwoo", 'utf_8')).hexdigest()
  
  if result[0][0] == hashedPW:
    return True
  else: 
    return False


# name 존재여부 검증
def isnameExist(name):
  cursor = dataBase.cursor()
  
  sql = ("SELECT EXISTS(SELECT * FROM student where name = %s)")
  val = [name]

  cursor.execute(sql, val)

  result = cursor.fetchall()
  for row in cursor:
    result.append(row)
  
  if result[0][0] >= 1:
    return True
  else:
    return False

# print(isnameExist('jiwoo'))


# json으로 데이터 전달
# jsonify_02 -> [["{}""], ["{}"], ["{}""]] 이런식으로 나오는데 header에 content-type은 json이라고 되어있음.
def returnJson(name):
  cursor = dataBase.cursor()
  sql = "SELECT JSON_OBJECT ('name', name, 'age', age, 'sex', sex, 'email', email, 'code', code, 'nickname', nickname, 'bio', bio) FROM student WHERE name = %s"
  val = [name]
  cursor.execute(sql, val)

  result = cursor.fetchall()
  for row in cursor:
    result.append(row)

  return jsonify(result)


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
  
  sql = "INSERT INTO student (name, age, sex, email, pw, code) VALUES(%s, %s, %s, %s, %s, %s)"
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


# READ
# 전체 학생 조회
@app.route("/student", methods=["GET"])
def student():
  cursor = dataBase.cursor()

  query = "SELECT JSON_OBJECT ('name', name, 'age', age, 'sex', sex, 'email', email, 'code', code, 'nickname', nickname, 'bio', bio) FROM student"
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



# UPDATE : error
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
      sql = "INSERT INTO student (nickname, bio) VALUES (%s, %s)"
      val = (body["nickname"], body["bio"])
      cursor.execute(sql, val)
      dataBase.commit()

      sql = "SELECT name, age, sex, email, code, nickname, bio FROM student WHERE name = %s"
      val = [name]
    
      cursor.execute(sql, val)

      result = cursor.fetchall()
      for name in cursor:
        result = name

      return str(result)

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
      sql = "DELETE FROM student WHERE name = (%s)"
      val = [name]
      cursor.execute(sql, val)

      dataBase.commit()

      return "DELETE!"

    else: 
      return "Wrong PW", 400

  else: 
    return "Wrong Name", 400

# dataBase.close()