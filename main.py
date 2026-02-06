from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LinearRegression
import numpy as np
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = "salary-db.c9usgw20qpyc.eu-north-1.rds.amazonaws.com"
DB_NAME = "salarydb"
DB_USER = "postgres"
DB_PASS = "Yildiz25"

def init_db():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            experience FLOAT,
            predicted_salary FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([30000, 35000, 42000, 50000, 58000, 65000, 73000, 80000, 88000, 95000])

model = LinearRegression()
model.fit(X, y)

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/style.css")
def css():
    return FileResponse("static/style.css")

@app.get("/app.js")
def js():
    return FileResponse("static/app.js")

@app.get("/predict")
def predict(experience: float):
    salary = float(round(model.predict([[experience]])[0], 2))

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute("INSERT INTO predictions (experience, predicted_salary) VALUES (%s, %s)", (experience, salary))
    conn.commit()
    cur.close()
    conn.close()

    return {
        "experience_years": experience,
        "predicted_salary": salary
    }

@app.get("/history")
def history():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute("SELECT experience, predicted_salary, created_at FROM predictions ORDER BY created_at DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"experience": r[0], "salary": r[1], "date": str(r[2])}
        for r in rows
    ]
