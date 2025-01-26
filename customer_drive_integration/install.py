import frappe
import uuid


def after_install():
    """
    Customizations to be applied after the app is installed.
    """
    # Add custom fields to the Customer Doctype
    add_custom_fields_to_customer()

    # Ensure Administrator's Drive exists
    ensure_administrator_drive_exists()


def add_custom_fields_to_customer():
    """
    Add custom fields to the Customer Doctype.
    """
    # Add the 'drive_link' field
    if not frappe.db.exists("Custom Field", {"dt": "Customer", "fieldname": "drive_link"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Customer",
            "fieldname": "drive_link",
            "fieldtype": "Data",
            "label": "Drive Link",
            "hidden": 1  # Make it hidden
        }).insert()

    # Add the 'Open Drive' button
    if not frappe.db.exists("Custom Field", {"dt": "Customer", "fieldname": "open_drive"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Customer",
            "fieldname": "open_drive",
            "fieldtype": "Button",
            "label": "Open Drive Folder"
        }).insert()


def ensure_administrator_drive_exists():
    """
    Ensure the Administrator's Drive exists in the system.
    """
    drive_title = "Administrator's Drive"
    if not frappe.db.exists("Drive Entity", {"title": drive_title, "is_group": 1}):
        # Create the main drive for Administrator
        frappe.get_doc({
            "doctype": "Drive Entity",
            "title": drive_title,
            "is_group": 1,
            "is_active": 1,
            "name": str(uuid.uuid4()),  # Set a unique name explicitly
            "file_kind": "Folder",  # Mark as folder
            "path": drive_title,
            "owner": "Administrator"  # Ensure the folder is owned by Administrator
        }).insert(ignore_permissions=True)
        frappe.msgprint(f"Drive folder '{drive_title}' has been created under Administrator.")
    else:
        frappe.msgprint(f"Drive folder '{drive_title}' already exists.")

