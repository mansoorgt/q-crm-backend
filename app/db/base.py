# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.position import Position  # noqa
from app.models.permission import Permission  # noqa
from app.models.role import Role  # noqa
from app.models.role_permission import role_permission  # noqa
from app.models.product import Product, Category, ProductStatus  # noqa
from app.models.customer import Customer, ContactPerson  # noqa
from app.models.inquiry import Inquiry  # noqa
from app.models.quotation import Quotation, QuotationItem  # noqa
from app.models.company_settings import CompanySettings  # noqa
from app.models.invoice import Invoice, InvoiceItem  # noqa
from app.models.supplier import Supplier  # noqa
from app.models.purchase_entry import PurchaseEntry, PurchaseEntryItem  # noqa
