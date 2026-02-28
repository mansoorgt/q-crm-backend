import sys

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        try:
            print("Creating permission and role_permission tables...")
            
            # Create permission table
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS permission (
                id INTEGER NOT NULL AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                description VARCHAR(255),
                PRIMARY KEY (id),
                UNIQUE INDEX ix_permission_name (name)
            ) ENGINE=InnoDB;
            """))

            # Create role_permission association table
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS role_permission (
                role_id INTEGER NOT NULL,
                permission_id INTEGER NOT NULL,
                PRIMARY KEY (role_id, permission_id),
                FOREIGN KEY(role_id) REFERENCES role (id) ON DELETE CASCADE,
                FOREIGN KEY(permission_id) REFERENCES permission (id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """))
            print("Successfully created new tables.")

            print("Seeding default permissions...")
            default_permissions = [
                ("dashboard_access", "Access to the Dashboard"),
                ("leads_access", "Access to Inquiries and Customers"),
                ("quotations_access", "Access to create and view Quotations"),
                ("invoices_access", "Access to handle Invoices"),
                ("reports_access", "Access to view Reports"),
                ("settings_access", "Access to System and User Settings"),
            ]
            for name, desc in default_permissions:
                conn.execute(
                    text("INSERT IGNORE INTO permission (name, description) VALUES (:name, :desc)"),
                    {"name": name, "desc": desc}
                )
            
            # Since dropping columns in MySQL might depend on keys, we just drop them if they exist
            print("Dropping old boolean columns from role table...")
            cols_to_drop = [
               "dashboard_access", "leads_access", "quotations_access", 
               "invoices_access", "reports_access", "settings_access"
            ]
            
            for col in cols_to_drop:
                try:
                    conn.execute(text(f"ALTER TABLE role DROP COLUMN {col};"))
                except Exception as ex:
                    print(f"Column {col} may not exist or could not be dropped: {ex}")

            print("Successfully migrated permissions structure.")
        except Exception as e:
            print("Migration failed:", e)

if __name__ == "__main__":
    migrate()
