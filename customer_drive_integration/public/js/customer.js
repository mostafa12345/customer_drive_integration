frappe.ui.form.on("Customer", {
    refresh: function (frm) {
        console.log("Customer Form Refreshed");
        console.log("Drive Link Value:", frm.doc.drive_link); // Log the drive_link value

        if (frm.doc.drive_link) {
            console.log("Drive Link exists. Adding button...");
            frm.add_custom_button("Open Drive Folder", () => {
                console.log("Button clicked. Opening Drive Link...");
                window.open(frm.doc.drive_link, "_blank"); // Open the folder link in a new tab
            });
        } else {
            console.log("Drive Link is not set for this customer.");
        }
    }
});

