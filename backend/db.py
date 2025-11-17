from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users = db["users"]
assignments = db["assignments"]
submissions = db["submissions"]
plag_reports = db["plag_reports"]
