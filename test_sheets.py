from app.google.sheets_service import get_client, SHEET_NAME

try:
    client = get_client()
    sheet = client.open(SHEET_NAME)
    print(f"Successfully connected to Google Sheet: {sheet.title}")
except Exception as e:
    print(f"Failed to connect: {e}")
