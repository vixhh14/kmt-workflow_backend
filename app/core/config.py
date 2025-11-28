
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_CREDS_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", r"C:/Users/Vishnu/Downloads/workflow-tracker1-a2972676dcb7.json")
SHEET_NAME = os.getenv("SHEET_NAME", "workflow_tracker")
JWT_SECRET = os.getenv("JWT_SECRET", "c2b0644eb4df8d087f994c58862a418fd455ac0286ee2bf3eec4e0e878328cde")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

CORS_ORIGINS = [
    "http://localhost:5173",
    "https://kmt-workflow-tracker-qayt.vercel.app",
]

