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
            existing_cps = db.query(ContactPerson).filter(ContactPerson.customer_id == db_obj.id).all()
            existing_cp_map = {cp.id: cp for cp in existing_cps}
             
            updated_cp_ids = set()
             
            for cp_data in contact_persons_data:
                if not isinstance(cp_data, dict):
                    cp_data = cp_data.dict(exclude_unset=True)
                     
                cp_id = cp_data.get('id')
                 
                if cp_id and cp_id in existing_cp_map:
                    # Update existing
                    existing_cp = existing_cp_map[cp_id]
                    for k, v in cp_data.items():
                        if k != 'id' and hasattr(existing_cp, k):
                            setattr(existing_cp, k, v)
                    updated_cp_ids.add(cp_id)
                else:
                    # Create new
                    cp_data.pop('id', None)
                    db.add(ContactPerson(**cp_data, customer_id=db_obj.id))
                     
            # Delete missing ones
            for cp_id, cp in existing_cp_map.items():
                if cp_id not in updated_cp_ids:
                    db.delete(cp)
                     
            try:
                db.commit()
                db.refresh(db_obj)
            except Exception as e:
                db.rollback()
                from sqlalchemy.exc import IntegrityError
                if isinstance(e, IntegrityError):
                    from fastapi import HTTPException
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Cannot delete contact person because it is referenced elsewhere."
                    )
                raise e

        return db_obj

customer = CRUDCustomer(Customer)
