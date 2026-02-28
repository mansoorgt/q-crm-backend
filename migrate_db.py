import os
import sys

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        try:
            # First, check if column exists
            # We are assuming MySQL based on standard pymysql DB URI
            print("Adding role_id to user table...")
            conn.execute(text("ALTER TABLE user ADD COLUMN role_id INTEGER DEFAULT NULL;"))
            conn.execute(text("ALTER TABLE user ADD CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES role(id);"))
            print("Successfully migrated user table.")
        except Exception as e:
            print("Migration failed or already applied:", e)

if __name__ == "__main__":
    migrate()
