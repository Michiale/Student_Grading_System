from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(50), unique=False, nullable=False)
    student_email = Column(String(50), unique=True, nullable=False)

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(String(50), primary_key=True, index=False)
    course_name = Column(String(50), unique=True, nullable=False)
    course_credits = Column(Integer, unique=False, nullable=False)

class Instructor(Base):
    __tablename__ = 'instructors'

    instructor_id = Column(String(50), primary_key=True, index=False)
    instructor_name = Column(String(50), unique=True, nullable=False)
    instructor_email = Column(String(50), unique=False, nullable=False)
    instructor_mobile_no = Column(Integer, unique=True)

