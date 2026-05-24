# Book Cover Validation System

## Setup

1. Install Python 3.x
2. Run: `pip install -r requirements.txt`
3. Create Airtable account and get API token
4. Create table with fields: Book ID (ISBN), Author Name, Author Email
5. Copy `.env.example` to `.env` and fill credentials
6. Run: `python main.py`

## Testing

Place sample covers in `tests/sample_covers/`

Run: `python main.py` and enter cover path and ISBN