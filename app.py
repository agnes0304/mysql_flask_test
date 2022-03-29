import mysql.connector

# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "<p>Hello!</p>"

dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="gg04236@@",
  database ="student"
)

cursor = dataBase.cursor()

query = ("SELECT * FROM student WHERE name = 'B'")
cursor.execute(query)

for (name) in cursor:
    print("{}".format(name))


cursor.close()
dataBase.close()