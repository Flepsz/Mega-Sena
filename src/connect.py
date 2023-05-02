import mysql.connector

con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='mega_sena'
)

cursor = con.cursor()
