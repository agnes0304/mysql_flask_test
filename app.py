from encodings import utf_8
import hashlib
import json
from itsdangerous import NoneAlgorithm
import mysql.connector
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def WELCOME():
    return "<p>WELCOME!</p>"


dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="gg04236@@",
  database ="SNU"
)


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

  sql = "SELECT * FROM student WHERE name = (%s)"
  val = [body["name"]]

  cursor.execute(sql, val)
  for name in cursor:
    print(name)


  return {'test': 10}


# READ
# 전체 학생 조회
@app.route("/student", methods=["GET"])
def student():
  cursor = dataBase.cursor()

  query = ("SELECT name, age, sex, email, nickname, bio FROM student")

  cursor.execute(query)

  result = cursor.fetchall()

  for name in cursor:
    result.append(name)

  return str(result)


# 학생 이름으로 조회
@app.route("/student/<name>", methods=["GET"])
def get_student_by_name(name):
  cursor = dataBase.cursor()

  sql = "SELECT name, age, sex, email, nickname, bio FROM student WHERE name = %s"
  val = [name]
  
  cursor.execute(sql, val)

  result = cursor.fetchall()
  for name in cursor:
    result = name

  return str(result)



# UPDATE
# 이름, pw입력 (pw는 json 형태로 받기)
@app.route("/student/<name>", methods=["PUT"])
def update_student_by_name(name):
  pass

# code 알고 있다고 가정
@app.route("/student/<code>", methods=["PUT"])
def update_student_by_code(code):
  pass



# DELETE
# 이름, pw입력 (pw는 json형태로 받기)
# 사용자 입력(request body)
# {
# 	"name": ,
# 	"pw": 
# }
@app.route("/student/<name>", methods=["DELETE"])
def delete_student_by_name(name):
  cursor = dataBase.cursor()

  sql = "SELECT pw from student WHERE name = %s"
  val = [name]

  cursor.execute(sql, val)

  result = cursor.fetchall()
  for name in cursor:
    result.append(name)
  
  print(result[0])

  body = request.get_json()
  hashedPW = hashlib.md5(bytes(body["pw"]+"jiwoo", 'utf_8')).hexdigest()
  
  if result[0] == hashedPW:
    sql = "DELETE FROM student WHERE name = (%s)"
    val = [name]
    cursor.execute(sql, val)

    dataBase.commit()

    return "DELETE!"

  else: 
    return "NO!", 400


# code 알고 있다고 가정
@app.route("/student/<code>", methods=["DELETE"])
def delete_student_by_code(code):
  pass



# dataBase.close()