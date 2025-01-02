import pymysql
db=pymysql.connect(
    host="localhost",
    user="chingiz",
    password="azar5408",
    database="chingiz_dev",
)
cursor=db.cursor()
