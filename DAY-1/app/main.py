from fastapi import FastAPI

app = FastAPI(title="FastAPI Day 1")

@app.get("/")
def home():
    return {"message": "FastAPI Day 1 setup successful 🚀"}
