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
  for (name) in cursor:
    print(name)

  dataBase.close()

  return {'test': 10}


# READ
# 전체 학생 조회
@app.route("/student", methods=["GET"])
def student():
  pass

# 학생 이름으로 조회
@app.route("/student/<name>", methods=["GET"])
def get_student_by_name(name):
  pass



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
@app.route("/student/<name>", methods=["DELETE"])
def delete_student_by_name(name):
  pass

# code 알고 있다고 가정
@app.route("/student/<code>", methods=["DELETE"])
def delete_student_by_code(code):
  pass



