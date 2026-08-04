# Google Sheets setup

The tracker appends newly discovered jobs to a worksheet named `Jobs`. Each row starts
with `Applied?` set to `No`, plus `Applied Date` and `Notes` columns for manual tracking.

1. Create a Google Sheet and copy its ID from the URL: the text between `/d/` and `/edit`.
2. In Google Cloud, create or select a project, enable the **Google Sheets API**, then create a service account and a JSON key for it.
3. Open the downloaded JSON and copy the `client_email` value. Share the Google Sheet with that email as an **Editor**.
4. In the GitHub repository, go to **Settings → Secrets and variables → Actions** and create these repository secrets:
   - `GOOGLE_SHEET_ID`: the Sheet ID from step 1.
   - `GOOGLE_SERVICE_ACCOUNT_JSON`: the entire JSON key file, including braces.
5. Run **IT Job Tracker** manually once from the GitHub Actions tab. The workflow creates the `Jobs` tab and its headers the first time it finds a new job.

Never commit the service-account JSON file to the repository.

## Local connection test

Before pushing to GitHub, create a local `.env` file (it is ignored by Git) with:

```dotenv
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SERVICE_ACCOUNT_FILE=/absolute/path/to/the-downloaded-key.json
```

Keep the downloaded key outside the repository. Then run:

```bash
pip install -r requirements.txt
python scripts/test_google_sheets.py
```

This creates the `Jobs` worksheet if needed and appends one row labelled
`TEST — Job Tracker` / `Dummy Job (safe to delete)`. Delete that row from Google
Sheets after confirming the connection works.
