from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base





class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(50), unique=False , nullable=False)
    student_email = Column( String(50), unique=True, nullable=False)

