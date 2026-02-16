import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.customer import Customer, ContactPerson

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    db = SessionLocal()
    
    # Create Customers
    customers = [
        {
            "name": "Acme Corp",
            "type": "company",
            "email": "contact@acme.com",
            "phone": "123-456-7890",
            "address": "123 Acne St, Looneyville",
            "contacts": [
                {"name": "Wile E. Coyote", "email": "wile@acme.com", "role": "Chief Buyer"},
                {"name": "Road Runner", "email": "beepbeep@acme.com", "role": "Tester"}
            ]
        },
        {
            "name": "Jane Doe",
            "type": "individual",
            "email": "jane@example.com",
            "phone": "555-0199",
            "address": "456 Individual Ln",
            "contacts": []
        }
    ]
    
    for c in customers:
        db_obj = db.query(Customer).filter(Customer.email == c["email"]).first()
        if not db_obj:
            db_obj = Customer(
                name=c["name"],
                type=c["type"],
                email=c["email"],
                phone=c["phone"],
                address=c["address"]
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Created customer: {c['name']}")
            
            for contact in c["contacts"]:
                cp = ContactPerson(
                    customer_id=db_obj.id,
                    name=contact["name"],
                    email=contact["email"],
                    role=contact["role"]
                )
                db.add(cp)
            db.commit()
            
    db.close()

if __name__ == "__main__":
    logger.info("Creating initial customer data")
    init_db()
    logger.info("Initial customer data created")
