from pyairtable import Table
import logging

class AirtableClient:
    def __init__(self, api_token, base_id, table_name):
        self.table = Table(api_token, base_id, table_name)
        self.logger = logging.getLogger(__name__)
    
    def get_author_by_isbn(self, isbn):
        try:
            formula = f"{{Book ID (ISBN)}} = '{isbn}'"
            records = self.table.all(formula=formula)
            if records:
                return records[0]['fields']
            return None
        except Exception as e:
            self.logger.error(f"Error fetching author: {e}")
            return None
    
    def create_or_update_record(self, isbn, author_name, author_email, status, confidence, issues, instructions):
        try:
            formula = f"{{Book ID (ISBN)}} = '{isbn}'"
            existing = self.table.all(formula=formula)
            
            fields = {
                "Book ID (ISBN)": isbn,
                "Author Name": author_name,
                "Author Email": author_email,
                "Status": status,
                "Confidence Score": confidence,
                "Issue Type": "Badge overlap" if "overlap" in str(issues).lower() else "Other",
                "Issue Details": ", ".join(issues) if issues else "No issues detected",
                "Correction Instructions": instructions,
                "Timestamp": ""
            }
            
            if existing:
                record_id = existing[0]['id']
                result = self.table.update(record_id, fields)
                self.logger.info(f"Updated record for ISBN: {isbn}")
            else:
                result = self.table.create(fields)
                self.logger.info(f"Created record for ISBN: {isbn}")
            
            return result
        except Exception as e:
            self.logger.error(f"Error with Airtable: {e}")
            return None