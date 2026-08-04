"""Google Sheets output for newly discovered jobs.

Required environment variables:
  GOOGLE_SHEET_ID               The ID in the spreadsheet URL.
  GOOGLE_SERVICE_ACCOUNT_JSON   The complete service-account JSON key.

The service account must have Editor access to the target spreadsheet.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
_WORKSHEET_NAME = "Jobs"
_HEADERS = [
    "First Seen",
    "Company",
    "Job Title",
    "Location",
    "Apply URL",
    "Source",
    "Applied?",
    "Applied Date",
    "Notes",
]


def _get_worksheet():
    sheet_id = os.environ["GOOGLE_SHEET_ID"].strip()
    credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not credentials_json:
        credentials_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        if not credentials_file:
            raise ValueError(
                "Set GOOGLE_SERVICE_ACCOUNT_JSON (for GitHub Actions) or "
                "GOOGLE_SERVICE_ACCOUNT_FILE (for local testing)."
            )
        credentials_json = Path(credentials_file).read_text(encoding="utf-8")
    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID is empty")

    credentials_info = json.loads(credentials_json)
    credentials = Credentials.from_service_account_info(
        credentials_info, scopes=_SCOPES
    )
    spreadsheet = gspread.authorize(credentials).open_by_key(sheet_id)

    try:
        return spreadsheet.worksheet(_WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=_WORKSHEET_NAME, rows=1000, cols=len(_HEADERS))


def _ensure_headers(worksheet) -> None:
    """Create headers only for a new/empty worksheet; never overwrite tracking data."""
    first_row = worksheet.row_values(1)
    if not first_row:
        worksheet.append_row(_HEADERS, value_input_option="USER_ENTERED")
    elif first_row != _HEADERS:
        raise ValueError(
            f"Worksheet '{_WORKSHEET_NAME}' has unexpected headers. "
            f"Expected: {_HEADERS}"
        )


def append_jobs(new_jobs: list[dict]) -> None:
    """Append all new jobs in one request and initialize application tracking."""
    worksheet = _get_worksheet()
    _ensure_headers(worksheet)
    if not new_jobs:
        print("  [Google Sheets] No new jobs to append.")
        return

    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = [
        [
            timestamp,
            job["company"],
            job["title"],
            job.get("location", ""),
            job.get("url", ""),
            job.get("source", ""),
            "No",  # Applied? — change to Yes in Google Sheets after applying
            "",  # Applied Date — set manually in Google Sheets
            "",  # Notes — set manually in Google Sheets
        ]
        for job in new_jobs
    ]
    worksheet.append_rows(rows, value_input_option="USER_ENTERED")
    print(f"  [Google Sheets] Appended {len(rows)} new job(s) to '{_WORKSHEET_NAME}'.")
