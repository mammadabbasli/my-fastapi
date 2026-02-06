from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([30000, 35000, 42000, 50000, 58000, 65000, 73000, 80000, 88000, 95000])

model = LinearRegression()
model.fit(X, y)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/predict")
def predict(experience: float):
    salary = model.predict([[experience]])[0]
    return {
        "experience_years": experience,
        "predicted_salary": round(salary, 2)
    }
