import logging

from app.db.session import SessionLocal
from app.models.product import Category, ProductStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    db = SessionLocal()
    
    # Create Statuses
    statuses = [
        {"name": "Active", "key": "active"},
        {"name": "Draft", "key": "draft"},
        {"name": "Archived", "key": "archived"},
    ]
    
    for s in statuses:
        db_obj = db.query(ProductStatus).filter(ProductStatus.key == s["key"]).first()
        if not db_obj:
            db_obj = ProductStatus(name=s["name"], key=s["key"])
            db.add(db_obj)
            logger.info(f"Created status: {s['name']}")
    
    # Create Categories
    categories = [
        {"name": "Electronics", "description": "Gadgets and devices"},
        {"name": "Clothing", "description": "Apparel and accessories"},
        {"name": "Services", "description": "Professional services"},
    ]
    
    for c in categories:
        db_obj = db.query(Category).filter(Category.name == c["name"]).first()
        if not db_obj:
            db_obj = Category(name=c["name"], description=c["description"])
            db.add(db_obj)
            logger.info(f"Created category: {c['name']}")
            
    db.commit()
    db.close()

if __name__ == "__main__":
    logger.info("Creating initial product data")
    init_db()
    logger.info("Initial product data created")
