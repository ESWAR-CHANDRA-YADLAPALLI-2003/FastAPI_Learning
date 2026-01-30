from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    password: str

class UserResponse(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    return user