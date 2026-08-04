"""Append one clearly labelled test row to the configured Google Sheet.

Run locally only after adding GOOGLE_SHEET_ID and GOOGLE_SERVICE_ACCOUNT_FILE
to a .env file. The .env file is ignored by Git.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

from notifier.google_sheets import append_jobs


append_jobs([
    {
        "company": "TEST — Job Tracker",
        "title": "Dummy Job (safe to delete)",
        "location": "Test location",
        "url": "https://example.com/test-job",
        "source": "manual test",
    }
])

print("Test complete. Check the 'Jobs' worksheet for the dummy row.")
