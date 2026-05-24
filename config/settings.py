import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN", "")
BASE_ID = os.getenv("BASE_ID", "")
TABLE_NAME = "Book Cover Validation"

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

SAFE_ZONE_MM = 3
BADGE_ZONE_MM = 9
COVER_WIDTH_INCH = 5
COVER_HEIGHT_INCH = 8

CONFIDENCE_THRESHOLD = 90