import click
import frappe
from customer_drive_integration.customer_drive import ensure_folder_exists, create_drive_folder, create_customer_structure

@click.command("create-folders-for-existing-customers")
@click.option("--site", help="Specify the site to run the command on")
def create_folders_for_existing_customers():
    """
    Create the predefined folder structure for all existing customers.
    """
    try:
        frappe.init(site=frappe.local.site)
        frappe.connect()

        # Ensure the main "Customer" folder exists under "Administrator's Drive"
        customer_folder = ensure_folder_exists("Customer", "Administrator's Drive")

        # Fetch all existing customers
        customers = frappe.get_all("Customer", fields=["name", "customer_name", "drive_link"])

        for customer in customers:
            print(f"Processing customer: {customer['customer_name']}")

            # Skip customers that already have a drive folder linked
            if customer["drive_link"]:
                print(f"Customer '{customer['customer_name']}' already has a drive folder. Skipping.")
                continue

            # Create the main folder for the customer
            customer_drive_folder = create_drive_folder(customer["customer_name"], customer_folder.name)

            # Update the 'Drive Link' field in the Customer doctype
            frappe.db.set_value("Customer", customer["name"], "drive_link", f"/drive/folder/{customer_drive_folder.name}")

            # Create the predefined folder structure under the customer's folder
            create_customer_structure(customer_drive_folder.name)

            print(f"Folders created for customer: {customer['customer_name']}")

        frappe.db.commit()
        print("Folder structure created for all existing customers.")
    except Exception as e:
        frappe.log_error(f"Error while creating folders for existing customers: {str(e)}", "Customer Drive Folder Creation")
        print(f"Error: {str(e)}")
    finally:
        frappe.destroy()

