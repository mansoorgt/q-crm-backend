import os
import sys

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        try:
            print("Adding stock_availability to quotationitem table...")
            conn.execute(text("ALTER TABLE quotationitem ADD COLUMN stock_availability VARCHAR(50) DEFAULT NULL;"))
            print("Successfully updated quotationitem table.")
        except Exception as e:
            print("Migration for quotationitem failed or already applied:", e)

        try:
            print("Adding stock_availability to invoiceitem table...")
            conn.execute(text("ALTER TABLE invoiceitem ADD COLUMN stock_availability VARCHAR(50) DEFAULT NULL;"))
            print("Successfully updated invoiceitem table.")
        except Exception as e:
            print("Migration for invoiceitem failed or already applied:", e)

if __name__ == "__main__":
    migrate()
