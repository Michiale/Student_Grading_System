from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Union
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class StudentBase(BaseModel):
    student_name: str
    student_email: str

class CourseBase(BaseModel):
    course_id: Union[str, int] 
    course_name: str
    course_credits: int

class InstructorBase(BaseModel):
    Instructor_id: Union[str, int]
    Instructor_name: str
    Instructor_email: Union[str,int]
    Instructor_mobail_no : int


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

@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseBase, db: db_dependency):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.post("/instructors", status_code=status.HTTP_201_CREATED)
async def create_instructor(instructor: InstructorBase, db: db_dependency):
    db_instructor = models.Instructor(**instructor.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
async def read_student(student_id:int, db: db_dependency ):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def read_course(course_id:Union[str, int], db: db_dependency ):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return course

@app.get("/instructors/{instructor_id}", status_code=status.HTTP_200_OK)
async def read_instructor(instructor_id:Union[str, int], db: db_dependency ):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.instructor_id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_instructor

@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int, db: db_dependency):
    db_student= db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

@app.delete("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(course_id: Union[str, int], db: db_dependency):
    db_course= db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_course)
    db.commit()
    return {"message": "Student deleted successfully"}

@app.delete("/instructors/{instructor_id}", status_code=status.HTTP_200_OK)
async def delete_instructor(instructor_id: Union[str, int], db: db_dependency):
    db_instructor= db.query(models.Instructor).filter(models.Instructor.instructor_id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_instructor)
    db.commit()
    return {"message": "instructor deleted successfully"}

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

@app.put("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def update_course(course_id: Union[str, int], update_course: CourseBase, db: db_dependency):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="course not found")
    
    for key, value in update_course.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    
    db.commit()
    db.refresh(course)
    return {"message": "Student updated successfully", "student": course}

@app.put("/instructors/{instructors_id}", status_code=status.HTTP_200_OK)
async def update_instructor(instructors_id: Union[str, int], update_instructor: InstructorBase, db: db_dependency):
    db_instructor= db.query(models.Instructor).filter(models.Instructor.instructor_id == instructors_id).first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="course not found")
    
    for key, value in update_instructor.model_dump(exclude_unset=True).items():
        setattr(db_instructor, key, value)
    
    db.commit()
    db.refresh(db_instructor)
    return {"message": "Student updated successfully", "student":db_instructor}












