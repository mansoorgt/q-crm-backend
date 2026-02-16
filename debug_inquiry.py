import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import enum

# Mocking the Enum to match user's code
class InquiryStatus(str, enum.Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    PROPOSAL_SENT = "Proposal Sent"
    CONVERTED = "Converted"
    LOST = "Lost"
    WON = "Won"

# Setup DB connection (assuming standard sqlite path or env)
# We need to find the database URL. Usually in .env or core/config.py
# For now, I'll try to guess or use the one from code if accessible.
# Let's read app/core/config.py or .env first? 
# I will assume sqlite:///./sql_app.db or similar if local.
# But let's look at where main.py runs.

# Let's try to import the Base/Session from app code to be sure.
sys.path.append(os.getcwd())
from app.db.session import SessionLocal

def check_data():
    db = SessionLocal()
    try:
        # Check raw values in DB
        print("--- Checking Raw Values in Inquiry Table ---")
        result = db.execute(text("SELECT id, status FROM inquiry"))
        for row in result:
            print(f"ID: {row.id}, Status: '{row.status}'")
            
            # Try mapping
            try:
                mapped = InquiryStatus(row.status)
                print(f"  -> Mapped to: {mapped}")
            except Exception as e:
                print(f"  -> FAILED to map: {e}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_data()
