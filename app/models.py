from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Create a declarative base class
Base = declarative_base()

# Define the Department model
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    department = Column(String, nullable=False)  # Department name column

    # Define relationship with Employee model
    employees = relationship("Employee", back_populates="department")

# Define the Job model
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    job = Column(String, nullable=False)  # Job title column

    # Define relationship with Employee model
    employees = relationship("Employee", back_populates="job")

# Define the Employee model
class Employee(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    name = Column(String, nullable=False)  # Employee's name column
    datetime = Column(String, nullable=False)  # Timestamp when the employee was hired
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)  # Foreign key to Department
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)  # Foreign key to Job

    # Define relationships
    department = relationship("Department", back_populates="employees")  # Relationship to Department
    job = relationship("Job", back_populates="employees")  # Relationship to Job
    