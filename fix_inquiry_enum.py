import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Setup DB connection
sys.path.append(os.getcwd())
from app.db.session import SessionLocal

def fix_data():
    db = SessionLocal()
    try:
        print("--- Fixing Inquiry Status Values ---")
        
        # Update Pending -> New
        result = db.execute(text("UPDATE inquiry SET status = 'New' WHERE status = 'Pending'"))
        print(f"Updated 'Pending' -> 'New': {result.rowcount} rows")
        
        # Update NEW -> New
        result = db.execute(text("UPDATE inquiry SET status = 'New' WHERE status = 'NEW'"))
        print(f"Updated 'NEW' -> 'New': {result.rowcount} rows")
        
        db.commit()
        print("Commit successful.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_data()
