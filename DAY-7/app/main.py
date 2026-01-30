from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -----------------
# Models
# -----------------

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class User(UserCreate):
    id: int

# -----------------
# In-memory storage
# -----------------

users: List[User] = []
current_id = 1

# -----------------
# CREATE
# -----------------

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global current_id
    new_user = User(id=current_id, **user.dict())
    users.append(new_user)
    current_id += 1
    return new_user

# -----------------
# READ ALL
# -----------------

@app.get("/users", response_model=List[User])
def get_users():
    return users

# -----------------
# READ ONE
# -----------------

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# -----------------
# UPDATE
# -----------------

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated: UserCreate):
    for index, user in enumerate(users):
        if user.id == user_id:
            updated_user = User(id=user_id, **updated.dict())
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# -----------------
# DELETE
# -----------------

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
