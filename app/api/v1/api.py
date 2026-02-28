from fastapi import APIRouter

from app.api.v1.endpoints import (
    login, users, positions, products, customers, 
    inquiries, quotations, company_settings, invoices,
    suppliers, purchase_entries, roles, permissions
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(inquiries.router, prefix="/inquiries", tags=["inquiries"])
api_router.include_router(quotations.router, prefix="/quotations", tags=["quotations"])
api_router.include_router(company_settings.router, prefix="/settings/company", tags=["company-settings"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(purchase_entries.router, prefix="/purchase-entries", tags=["purchase-entries"])
