from app.crud.base import CRUDBase
from app.models.inquiry import Inquiry
from app.models.customer import Customer
from app.schemas.inquiry import InquiryCreate, InquiryUpdate
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, String

class CRUDInquiry(CRUDBase[Inquiry, InquiryCreate, InquiryUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, search: str = "") -> list[Inquiry]:
        query = db.query(self.model).outerjoin(Customer)
        if search:
            query = query.filter(
                or_(
                    self.model.id.cast(String).ilike(f"%{search}%"),
                    Customer.name.ilike(f"%{search}%"),
                )
            )
        return query.order_by(desc(self.model.id)).offset(skip).limit(limit).all()

    def count(self, db: Session, search: str = "") -> int:
        query = db.query(self.model).outerjoin(Customer)
        if search:
            query = query.filter(
                or_(
                    self.model.id.cast(String).ilike(f"%{search}%"),
                    Customer.name.ilike(f"%{search}%"),
                )
            )
        return query.count()

inquiry = CRUDInquiry(Inquiry)
