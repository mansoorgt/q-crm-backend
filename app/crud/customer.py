from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.customer import Customer, ContactPerson
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> List[Customer]:
        query = db.query(self.model)
        if search:
            query = query.filter(self.model.name.ilike(f"%{search}%"))
        return query.offset(skip).limit(limit).all()

    def create_with_contact_persons(
        self, db: Session, *, obj_in: CustomerCreate
    ) -> Customer:
        obj_in_data = obj_in.dict()
        contact_persons_data = obj_in_data.pop("contact_persons", [])
        
        db_obj = Customer(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        for cp_data in contact_persons_data:
            contact_person = ContactPerson(**cp_data, customer_id=db_obj.id)
            db.add(contact_person)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def update_with_contact_persons(
        self, db: Session, *, db_obj: Customer, obj_in: Union[CustomerUpdate, Dict[str, Any]]
    ) -> Customer:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        contact_persons_data = update_data.pop("contact_persons", None)
        
        # Update Customer basic info
        db_obj = super().update(db, db_obj=db_obj, obj_in=update_data)
        
        # Handle Contact Persons if provided
        if contact_persons_data is not None:
             # Basic strategy: Delete all existing and re-create (simplest for now)
             # Or smarter: update existing, delete missing, create new.
             # For MVP, let's keep it simple: clear and re-add or just add new ones? 
             # The user requirement implies managing them.
             
             # Let's try to match by ID if possible, but the schema assumes just data.
             # If we want full sync, we might need a more complex update.
             # For now, let's assume we preserve existing ones and adding/updating is handled separately or
             # we wipe and replace? Wiping and replacing is destructive if IDs change.
             # Let's assume the update payload expects the full list of desired state?
             # If we receive contact_persons, we should probably align with that list.
             
             # Deleting all existing for this customer
            db.query(ContactPerson).filter(ContactPerson.customer_id == db_obj.id).delete()
            
            for cp_data in contact_persons_data:
                 # cp_data might have 'id' but we just re-create for simplicity in this MVP approach 
                 # unless we strictly need to keep IDs.
                 # Filter out 'id' if present in dict to avoid collision or error if we treat as new
                 if isinstance(cp_data, dict):
                    cp_data.pop('id', None)
                 else:
                    # pydantic model
                    cp_data = cp_data.dict(exclude={'id'})
                 
                 contact_person = ContactPerson(**cp_data, customer_id=db_obj.id)
                 db.add(contact_person)
            
            db.commit()
            db.refresh(db_obj)

        return db_obj

customer = CRUDCustomer(Customer)
