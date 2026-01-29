from fastapi import FastAPI

app=FastAPI()

@app.get("/users/{id}")
def get_user_details(id: int, active: bool = True):
    return {
        "user_id": id,
        "active": active
    }
