from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Pydantic Models
# -----------------------------

# Used when creating a student
class StudentCreate(BaseModel):
    id: int
    name: str
    age: int

# Used when updating a student (ID is NOT allowed to change)
class StudentUpdate(BaseModel):
    name: str
    age: int

# Internal model (what we store)
class Student(BaseModel):
    id: int
    name: str
    age: int

# -----------------------------
# In-memory storage (RAM)
# -----------------------------
# Create an empty list named students that will store Student objects
students: list[Student] = []

# -----------------------------
# CREATE Student
# -----------------------------
@app.post("/students", status_code=201)
def create_student(student: StudentCreate):

    # Check for duplicate ID
    for s in students:
        if s.id == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student with this ID already exists"
            )

    # Convert input model to internal model
    new_student = Student(
        id=student.id,
        name=student.name,
        age=student.age
    )

    students.append(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }

# -----------------------------
# GET All Students
# -----------------------------
@app.get("/students")
def get_students():
    return students

# -----------------------------
# GET Student by ID
# -----------------------------
@app.get("/students/{student_id}")
def get_student(student_id: int):

    for s in students:
        if s.id == student_id:
            return s

    # Proper REST error
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

# -----------------------------
# UPDATE Student
# -----------------------------
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_data: StudentUpdate):

    for index, s in enumerate(students):

        if s.id == student_id:

            # Update ONLY allowed fields
            students[index].name = updated_data.name
            students[index].age = updated_data.age

            return {
                "message": "Student updated successfully",
                "student": students[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

# -----------------------------
# DELETE Student
# -----------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, s in enumerate(students):
        if s.id == student_id:
            students.pop(index)
            return {"message": "Student deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
