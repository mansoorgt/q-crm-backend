import os
import sys

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        try:
            print("Adding bank_charges to quotation table...")
            conn.execute(text("ALTER TABLE quotation ADD COLUMN bank_charges FLOAT DEFAULT 0.0;"))
            print("Successfully updated quotation table.")
        except Exception as e:
            print("Migration for quotation failed or already applied:", e)

        try:
            print("Adding bank_charges to invoice table...")
            conn.execute(text("ALTER TABLE invoice ADD COLUMN bank_charges FLOAT DEFAULT 0.0;"))
            print("Successfully updated invoice table.")
        except Exception as e:
            print("Migration for invoice failed or already applied:", e)

if __name__ == "__main__":
    migrate()
