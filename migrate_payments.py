import os
import sys

from sqlalchemy import inspect
from app.db.session import engine
from app.models.invoice import InvoicePayment

def migrate():
    # create the table if it doesnt exist
    print("Creating InvoicePayment table...")
    InvoicePayment.__table__.create(engine, checkfirst=True)
    print("Successfully created InvoicePayment table.")

if __name__ == "__main__":
    migrate()
