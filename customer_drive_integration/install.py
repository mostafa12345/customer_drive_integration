import frappe

def after_install():
    """
    Customizations to be applied after the app is installed.
    """
    # Add the 'drive_link' field to the Customer Doctype
    if not frappe.db.exists("Custom Field", {"dt": "Customer", "fieldname": "drive_link"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Customer",
            "fieldname": "drive_link",
            "fieldtype": "Data",
            "label": "Drive Link",
            "hidden": 1  # Make it hidden
        }).insert()

    # Add the 'Open Drive' button to the Customer Doctype
    if not frappe.db.exists("Custom Field", {"dt": "Customer", "fieldname": "open_drive"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Customer",
            "fieldname": "open_drive",
            "fieldtype": "Button",
            "label": "Open Drive Folder"  # Fixed missing comma here
        }).insert()

