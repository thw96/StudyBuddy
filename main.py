from fastapi import FastAPI, Depends, HTTPException, status, Query , BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timedelta
import os

import asyncio
import sys
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

login_data = pd.read_csv("users.csv",delimiter=',')
grades = pd.read_csv("grades.csv",delimiter=',')
student = pd.read_csv("student.csv",delimiter=',')

class LoginRequest(BaseModel):
    user_id: str
    password: str

class Summary(BaseModel):
    user_id: str

# User login
@app.post("/login")
def login(login_request: LoginRequest):
    #print(login_data['password'])
    user_exists = ((login_data['user_id'] == login_request.user_id) & 
                   (login_data['password'] == login_request.password)).any()
    print(user_exists)
    if user_exists:
        return {"status": True, "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# User summary (GPA)
@app.post("/summary")
def summary_gpa(summary: Summary):
    gpa = student.loc[student["student_id"] == summary.user_id, "gpa"].values
    student_data = student[student["student_id"] == summary.user_id]

    if gpa.size > 0:
        gpa_value = gpa[0]
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
    completed_courses = student.loc[student["student_id"] == summary.user_id, "completed"].values
    completed_count = completed_courses[0] if completed_courses.size > 0 else 0

    return {"c_gpa": gpa_value, "c_courses": completed_count}

# User current courses
@app.post("/courses")
def summary_courses(summary: Summary):
    current_courses = grades[grades['student_id'] == summary.user_id]['subject_id'].unique()

    return {"current_courses": current_courses.tolist()}

