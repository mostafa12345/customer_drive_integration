import frappe
import uuid

def upload_to_customer_drive(doc, method):
    """
    Upload a file to the corresponding Drive folder for a customer.
    """
    frappe.log_error(f"File upload triggered: {doc.name}", "File Upload Debugging")
    try:
        if doc.attached_to_doctype == "Customer" and doc.attached_to_name:
            customer_name = doc.attached_to_name
            frappe.log_error(f"File linked to Customer: {customer_name}", "File Upload Debugging")

            # Retrieve the drive link for the customer
            drive_link = frappe.db.get_value("Customer", customer_name, "drive_link")
            frappe.log_error(f"Drive link found: {drive_link}", "File Upload Debugging")

            if not drive_link:
                frappe.throw(f"No Drive folder found for customer '{customer_name}'.")

            drive_entity_id = drive_link.split("/")[-1]
            frappe.log_error(f"Drive Entity ID: {drive_entity_id}", "File Upload Debugging")

            if frappe.db.exists("Drive Entity", drive_entity_id):
                parent_drive_entity = frappe.get_doc("Drive Entity", drive_entity_id)
                frappe.log_error(f"Parent Drive Entity: {parent_drive_entity.name}", "File Upload Debugging")

                # Ensure the file is uploaded under "Mohamed Elshelawy's Drive"
                parent_path = f"{parent_drive_entity.path}/{doc.file_name}"
                unique_name = str(uuid.uuid4())

                # Create a new file entity
                new_file = frappe.get_doc({
                    "doctype": "Drive Entity",
                    "title": doc.file_name,
                    "is_group": 0,
                    "is_active": 1,
                    "parent_drive_entity": parent_drive_entity.name,
                    "name": unique_name,
                    "file_kind": "File",
                    "path": parent_path,
                    "document": doc.name,
                    "mime_type": doc.content_type,
                    "owner": "Mohamed Elshelawy"  # Ensure the owner is set correctly
                })
                new_file.insert(ignore_permissions=True)
                frappe.db.commit()

                frappe.msgprint(f"File '{doc.file_name}' successfully uploaded to Drive for customer '{customer_name}'.")
            else:
                frappe.throw(f"Drive Entity '{drive_entity_id}' does not exist.")
    except Exception as e:
        frappe.log_error(f"Error in upload_to_customer_drive: {str(e)}", "File Upload Debugging")

