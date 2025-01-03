import pymysql

def get_db_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            port=3307,
            database="chingiz_dev",
        )
        return connection
    except pymysql.MySQLError as e:
        print("MySQL bilan bog'lanishda xatolik:", e)
        return None

