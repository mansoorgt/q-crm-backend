import os
import sys

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        try:
            print("Creating purchaseentryattachment table...")
            conn.execute(text("""
            CREATE TABLE purchaseentryattachment (
                id SERIAL PRIMARY KEY,
                purchase_entry_id INTEGER NOT NULL REFERENCES purchaseentry(id) ON DELETE CASCADE,
                file_name VARCHAR(255) NOT NULL,
                file_url VARCHAR(500) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))
            print("Successfully created purchaseentryattachment table.")
        except Exception as e:
            print("Migration failed or already applied:", e)

if __name__ == "__main__":
    migrate()
