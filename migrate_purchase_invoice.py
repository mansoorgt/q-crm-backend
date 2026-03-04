import os
import sys

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        try:
            print("Adding invoice_id to purchaseentry table...")
            conn.execute(text("ALTER TABLE purchaseentry ADD COLUMN invoice_id INTEGER REFERENCES invoice(id);"))
            print("Successfully updated purchaseentry table.")
        except Exception as e:
            print("Migration for purchaseentry failed or already applied:", e)

if __name__ == "__main__":
    migrate()
