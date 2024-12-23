import uvicorn
from fastapi import FastAPI
import pymysql
app = FastAPI()
db=pymysql.connect(
    host="mysql-chingiz.alwaysdata.net",
    database="chingiz_dev",
    user="chingiz",
    password="azar5408"
)
cursor=db.cursor()
@app.get("/items")
async def index():
    cursor.execute("select * from men")
    result=cursor.fetchall()
    return {result}
@app.get("/welcome")
async def welcome():
    return {"message": "This is the /welcome path"}
if __name__ == "__main__":
 uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
