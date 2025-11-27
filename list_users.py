"""
Script to list ALL users in the Google Sheet.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.google import sheets_service

def list_users():
    print("Fetching all users from Google Sheets...", flush=True)
    print("-" * 50, flush=True)
    
    try:
        users = sheets_service.get_users()
        print(f"Found {len(users)} users:", flush=True)
        for u in users:
            print(u, flush=True)
            
        if not users:
            print("⚠️  No users found! The sheet might be empty.", flush=True)
            
    except Exception as e:
        print(f"❌ Error fetching users: {str(e)}", flush=True)

if __name__ == "__main__":
    list_users()
