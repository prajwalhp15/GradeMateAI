import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_grader")
DB_NAME = os.getenv("DB_NAME", "ai_grader")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Runner / sandbox config
RUN_TIMEOUT = int(os.getenv("RUN_TIMEOUT", 5))  # seconds
MAX_OUTPUT_SIZE = int(os.getenv("MAX_OUTPUT_SIZE", 2000))  # chars
