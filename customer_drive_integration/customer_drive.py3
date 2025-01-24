import frappe
import uuid


def create_customer_drive_folder(doc, method):
    """
    Create a Drive folder for a customer with a predefined folder structure and save its link.
    """
    try:
        # Ensure the 'Customer' folder exists under 'Mohamed Elshelawy's Drive'
        owner_drive_folder = frappe.db.get_value("Drive Entity", {"title": "Mohamed Elshelawy's Drive", "is_group": 1})
        if not owner_drive_folder:
            frappe.throw("Mohamed Elshelawy's Drive folder does not exist. Please create it manually.")

        customer_folder = ensure_folder_exists("Customer", owner_drive_folder)

        # Check if a folder for this customer already exists
        if not frappe.db.exists("Drive Entity", {"title": doc.customer_name, "parent_drive_entity": customer_folder.name}):
            # Create the main customer folder
            customer_drive_folder = create_drive_folder(doc.customer_name, customer_folder.name)

            # Save the link in the Customer's 'Drive Link' field
            doc.db_set("drive_link", f"/drive/folder/{customer_drive_folder.name}")
            frappe.msgprint(f"Drive folder created for customer '{doc.customer_name}'.")

            # Create the folder structure under the customer's folder
            create_customer_structure(customer_drive_folder.name)

    except Exception as e:
        frappe.log_error(f"Error creating drive folder for customer '{doc.customer_name}': {str(e)}", "Customer Drive Creation")


def ensure_folder_exists(title, parent_id):
    """
    Ensure a folder exists, or create it if not found.
    """
    folder = frappe.db.get_value("Drive Entity", {"title": title, "is_group": 1, "parent_drive_entity": parent_id}, "name")
    if not folder:
        folder = create_drive_folder(title, parent_id).name
    return frappe.get_doc("Drive Entity", folder)


def create_drive_folder(title, parent_id):
    """
    Create a folder in the Drive module using Drive Entity.

    :param title: Name of the new folder to create.
    :param parent_id: Parent folder ID under which the new folder will be created.
    """
    unique_name = str(uuid.uuid4())
    new_folder = frappe.get_doc({
        "doctype": "Drive Entity",
        "title": title,
        "is_group": 1,
        "is_active": 1,
        "parent_drive_entity": parent_id,
        "name": unique_name,
        "file_kind": "Folder",  # Mark as folder
        "path": f"{parent_id}/{title}"
    })
    new_folder.insert(ignore_permissions=True)
    frappe.db.commit()
    return new_folder


def create_customer_structure(customer_folder_id):
    """
    Create the predefined folder structure under the customer folder.

    :param customer_folder_id: The unique ID of the customer's main folder.
    """
    folder_structure = {
        "CSD": {
            "Customer Advisory": [],
            "Account Executive": [
                "Marketing",
                "Offers",
                "BRS and Design",
                "Procurement"
            ]
        },
        "PMO": ["Agile", "Waterfall"],
        "COE": ["Supply Chain", "Collection", "Legal and Contract"],
        "TOC": [
            "Cloud Ops",
            "Service Disk",
            "General SOC",
            "DevOps",
            "Cyber SOC"
        ]
    }

    for folder, subfolders in folder_structure.items():
        main_folder = create_drive_folder(folder, customer_folder_id)

        if isinstance(subfolders, list):
            for subfolder in subfolders:
                create_drive_folder(subfolder, main_folder.name)
        elif isinstance(subfolders, dict):
            for subfolder, sub_subfolders in subfolders.items():
                subfolder_obj = create_drive_folder(subfolder, main_folder.name)
                for sub_subfolder in sub_subfolders:
                    create_drive_folder(sub_subfolder, subfolder_obj.name)


def create_folders_for_existing_customers():
    """
    Create folders for all existing customers in the system with the predefined structure.
    """
    try:
        # Fetch all existing customers
        customers = frappe.get_all("Customer", fields=["name", "customer_name", "drive_link"])

        for customer in customers:
            # Skip customers who already have a drive folder
            if customer.get("drive_link"):
                frappe.msgprint(f"Skipping customer '{customer['customer_name']}' (already has a drive folder).")
                continue

            # Get the Customer document
            customer_doc = frappe.get_doc("Customer", customer["name"])

            # Create the folder and structure for the customer
            create_customer_drive_folder(customer_doc, method="after_insert")

        frappe.msgprint("Folders created for all existing customers.")
    except Exception as e:
        frappe.log_error(f"Error creating folders for existing customers: {str(e)}", "Customer Drive Creation for Existing Customers")
        frappe.throw("An error occurred while creating folders for existing customers.")

