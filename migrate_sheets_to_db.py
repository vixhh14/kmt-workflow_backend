"""
Script to migrate data from Google Sheets to SQLite.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.models_db import Machine, Task, OutsourceItem
from app.google import sheets_service
import uuid
from datetime import datetime

def migrate_data():
    print("Starting data migration from Google Sheets to SQLite...", flush=True)
    db = SessionLocal()
    
    try:
        # 1. Migrate Machines
        print("Fetching Machines from Sheets...", flush=True)
        machines_data = sheets_service.get_machines()
        print(f"Found {len(machines_data)} machines.", flush=True)
        
        for m in machines_data:
            # Check if exists
            if not db.query(Machine).filter(Machine.id == m['id']).first():
                new_machine = Machine(
                    id=m['id'],
                    name=m['name'],
                    status=m['status'],
                    hourly_rate=float(m.get('hourly_rate', 0)),
                    last_maintenance=m.get('last_maintenance')
                )
                db.add(new_machine)
        print("✅ Machines migrated.", flush=True)

        # 2. Migrate Tasks
        print("Fetching Tasks from Sheets...", flush=True)
        tasks_data = sheets_service.get_tasks()
        print(f"Found {len(tasks_data)} tasks.", flush=True)
        
        for t in tasks_data:
            if not db.query(Task).filter(Task.id == t['id']).first():
                new_task = Task(
                    id=t['id'],
                    title=t['title'],
                    description=t.get('description'),
                    status=t['status'],
                    priority=t['priority'],
                    assigned_to=t.get('assigned_to'),
                    machine_id=t.get('machine_id'),
                    due_date=t.get('due_date'),
                    created_at=datetime.utcnow() # We don't have created_at in sheets, using now
                )
                db.add(new_task)
        print("✅ Tasks migrated.", flush=True)

        # 3. Migrate Outsource Items
        print("Fetching Outsource Items from Sheets...", flush=True)
        outsource_data = sheets_service.get_outsource_items()
        print(f"Found {len(outsource_data)} items.", flush=True)
        
        for o in outsource_data:
            if not db.query(OutsourceItem).filter(OutsourceItem.id == o['id']).first():
                new_item = OutsourceItem(
                    id=o['id'],
                    title=o['title'],
                    vendor=o['vendor'],
                    status=o['status'],
                    cost=float(o.get('cost', 0)),
                    expected_date=o.get('expected_date')
                )
                db.add(new_item)
        print("✅ Outsource Items migrated.", flush=True)
        
        db.commit()
        print("\n🎉 MIGRATION COMPLETE! All data is now in SQLite.", flush=True)
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}", flush=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_data()
