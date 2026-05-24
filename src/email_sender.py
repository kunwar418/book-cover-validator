import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.logger = logging.getLogger(__name__)
    
    def send_validation_email(self, to_email, author_name, status, issues, confidence):
        subject = f"Book Cover Validation Result: {status}"
        
        if status == "PASS":
            body = f"""
Dear {author_name},

Your book cover has been validated and PASSED all quality checks.

Status: {status}
Confidence Score: {confidence}%

No issues were detected. Your cover is ready for publication.

If you have any questions, please contact us at support@bookleafpub.com.

Best regards,
BookLeaf Publishing Team
"""
        else:
            instructions = "\n".join([f"- {issue}" for issue in issues])
            body = f"""
Dear {author_name},

Your book cover requires review.

Status: {status}
Confidence Score: {confidence}%

Issues detected:
{instructions}

Correction Instructions:
1. Ensure author name does not overlap with the award badge area (bottom 9mm of cover)
2. Maintain 3mm margins on all sides
3. Ensure resolution is at least 150 DPI
4. Resubmit corrected cover to the Google Drive folder within 3 days

For assistance, reply to this email or contact support@bookleafpub.com.

Best regards,
BookLeaf Publishing Team
"""
        
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            self.logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False