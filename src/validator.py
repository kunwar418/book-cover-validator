import logging
from src.image_processor import ImageProcessor
from src.airtable_client import AirtableClient
from src.email_sender import EmailSender

class Validator:
    def __init__(self, airtable_client, email_sender):
        self.image_processor = ImageProcessor()
        self.airtable_client = airtable_client
        self.email_sender = email_sender
        self.logger = logging.getLogger(__name__)
    
    def process_cover(self, image_path, isbn):
        self.logger.info(f"Processing cover: {image_path} for ISBN: {isbn}")
        
        author_data = self.airtable_client.get_author_by_isbn(isbn)
        
        if not author_data:
            self.logger.error(f"Author not found for ISBN: {isbn}")
            return False
        
        author_name = author_data.get('Author Name', 'Author')
        author_email = author_data.get('Author Email', '')
        
        if not author_email:
            self.logger.error(f"No email found for ISBN: {isbn}")
            return False
        
        result = self.image_processor.validate_cover(image_path)
        
        status = result['status']
        confidence = result['confidence']
        issues = result['issues']
        
        if status == "PASS":
            instructions = "No corrections needed. Your cover is approved."
        else:
            instructions = "Please correct the issues listed above and resubmit."
        
        self.airtable_client.create_or_update_record(
            isbn, author_name, author_email, status, confidence, issues, instructions
        )
        
        self.email_sender.send_validation_email(
            author_email, author_name, status, issues, confidence
        )
        
        self.logger.info(f"Processing complete for {isbn}: {status}")
        return True