import os
import sys
import logging
from config.settings import *
from src.airtable_client import AirtableClient
from src.email_sender import EmailSender
from src.validator import Validator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_single_cover(image_path, isbn):
    airtable = AirtableClient(AIRTABLE_TOKEN, BASE_ID, TABLE_NAME)
    emailer = EmailSender(EMAIL_SENDER, EMAIL_PASSWORD)
    validator = Validator(airtable, emailer)
    
    return validator.process_cover(image_path, isbn)

def main():
    print("\n" + "="*50)
    print("BOOK COVER VALIDATION SYSTEM")
    print("="*50)
    
    print("\nEnter cover details:")
    image_path = input("Cover image path: ").strip()
    isbn = input("ISBN (13 digits): ").strip()
    
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return
    
    if len(isbn) not in [10, 13]:
        print(f"Warning: ISBN {isbn} seems invalid (should be 10 or 13 digits)")
    
    print("\nProcessing...")
    success = process_single_cover(image_path, isbn)
    
    if success:
        print("\n✓ Validation complete! Check logs for details.")
    else:
        print("\n✗ Validation failed. Check logs for errors.")

if __name__ == "__main__":
    main()