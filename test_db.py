import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.0.20",
  user="root",
  password="",
  database="china"
)

mycursor = mydb.cursor()

id = 543513627794210825

mycursor.execute(f"SELECT * FROM social_credit WHERE id = {id};")

fetch = mycursor.fetchall()


print(len(fetch))