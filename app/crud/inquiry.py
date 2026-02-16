from app.crud.base import CRUDBase
from app.models.inquiry import Inquiry
from app.schemas.inquiry import InquiryCreate, InquiryUpdate

class CRUDInquiry(CRUDBase[Inquiry, InquiryCreate, InquiryUpdate]):
    pass

inquiry = CRUDInquiry(Inquiry)
