from bson.objectid import ObjectId
from .db import users, assignments, submissions, plag_reports
import datetime
import bcrypt

# Simple user functions (passwords hashed for demo)
def create_user(email, username, password, role="student", extra=None):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    doc = {
        "email": email,
        "username": username,
        "password": hashed,
        "role": role,
        "extra": extra or {},
        "created_at": datetime.datetime.utcnow()
    }
    return users.insert_one(doc).inserted_id

def find_user_by_email(email):
    return users.find_one({"email": email})

def verify_password(user_doc, password):
    return bcrypt.checkpw(password.encode(), user_doc["password"])

# Assignments
def create_assignment(title, description, tests, deadline):
    doc = {
        "title": title,
        "description": description,
        "tests": tests,  # list of {"input":"", "expected":""}
        "deadline": deadline,
        "created_at": datetime.datetime.utcnow()
    }
    return assignments.insert_one(doc).inserted_id

def get_assignment(aid):
    return assignments.find_one({"_id": ObjectId(aid)})

# Submissions
def save_submission(student_email, assignment_id, language, code, result):
    doc = {
        "student_email": student_email,
        "assignment_id": ObjectId(assignment_id),
        "language": language,
        "code": code,
        "result": result,
        "created_at": datetime.datetime.utcnow()
    }
    return submissions.insert_one(doc).inserted_id
