import mysql.connector

from flask import Flask

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

cursor = dataBase.cursor()



# CREATE
@app.route("/student", methods=["POST"])
def add_student():
  pass



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




query = ("SELECT * FROM student WHERE name = 'B'")
cursor.execute(query)

for (name) in cursor:
    print("{}".format(name))

cursor.close()

dataBase.close()