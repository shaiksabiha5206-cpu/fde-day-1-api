# to install fastapi 1st python -m pip install fastapi uvicorn
# to run python -m  uvicorn file name without .py :app --reload
#pip install pydantic
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
app = FastAPI(title="fde day2")
def get():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "sabiha@12345",
        database ="fde_db"
    )
class Query(BaseModel):
    question: str
class CustomerSolver:
    def solve(self,question:str):
        if "refund" in question.lower():
            return "refund will be in 3 days!"
        elif "docker" in question.lower():
            return "docker is installing ,please wait"
        elif "api" in question.lower():
            return "api is still working dont be panic"
        else:
            return "our team will call"
solver = CustomerSolver()
@app.get("/")
def home():
    return {"message":"i am fde ,api is working"}
@app.post("/solve-query")
def solve_query(question:str):
    answer = solver.solve(question)
    #return{"question":question,"answer":answer}
    try:
        conn = get()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logs(id INT AUTO_INCREMENT PRIMARY KEY,question VARCHAR(255),answer VARCHAR(255))")
        cursor.execute("INSERT INTO logs(question,answer) VALUES(%s,%s)",(question,answer))
        cursor.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return {"error":str(e)}
    return {"question":question,"answer":answer}
@app.get("/history")
def get_history():
    conn = get()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"history":rows}

