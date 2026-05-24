# Book Cover Validation System

Automated system to detect book cover layout issues, specifically author name overlapping with award badge area.

## Features

- Resolution check (minimum 1200x1800 pixels required)
- Badge area overlap detection (bottom 9mm reserved for award badge)
- Text detection and density analysis
- Confidence scoring (0-100 percent)
- Status classification (PASS / REVIEW NEEDED)

## Setup

1. Install Python 3.x
2. Install dependencies:
    pip install -r requirements.txt

## How to Run

### Single Cover Validation
    python test_local.py


Enter the path to your cover image when prompted.

### Example Output
==================================================
    COVER VALIDATION RESULTS
==================================================
Image dimensions: 953 x 754 pixels
Estimated DPI: 191
Resolution: FAIL (Too low)
Text detected: Yes (density: 5.8)
Badge area occupied: Possible overlap (brightness: 12%)

STATUS: REVIEW NEEDED
CONFIDENCE: 40%
ISSUES: Low resolution, Potential overlap with badge area



## Test Results

| Image | Resolution | Badge Area Brightness | Status |
|-------|------------|----------------------|--------|
| image (36) (2).png | 953x754 | 12% | REVIEW NEEDED |

## Project Structure
    book_cover_validator/
├── test_local.py # Main validation script
├── main.py # Full system with Airtable integration
├── requirements.txt # Dependencies
├── sample covers/ # Test images folder
└── logs/ # Log files


## Detection Logic

1. Resolution Check: Image must be at least 1200x1800 pixels
2. Badge Zone: Bottom 9mm area reserved for award badge
3. Overlap Detection: Brightness below 50 percent indicates text overlap
4. Confidence Scoring: 100 percent minus penalties for each violation

## Requirements

- opencv-python
- numpy
- pillow

## GitHub Repository

https://github.com/kunwar418/book-cover-validator