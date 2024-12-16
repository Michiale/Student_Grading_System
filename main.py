from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

class StudentBase(BaseModel):
    student_name: str
    student_email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentBase, db: db_dependency):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
async def read_student(student_id:int, db: db_dependency ):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int, db: db_dependency):
    db_student= db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}





@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(student_id: int, update_student: StudentBase, db: db_dependency):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in update_student.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    return {"message": "Student updated successfully", "student": student}

















