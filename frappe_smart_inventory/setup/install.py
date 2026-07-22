import frappe

def after_install():
    """Hook ejecutable tras instalar la app vía 'bench install-app'"""
    create_default_custom_fields()
    create_sample_workspaces()
    frappe.logger().info("App frappe_smart_inventory configurada exitosamente.")

def create_default_custom_fields():
    """Crea Custom Fields en el DocType Batch de ERPNext si no existen"""
    if not frappe.db.exists("Custom Field", "Batch-custom_quality_status"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Batch",
            "fieldname": "custom_quality_status",
            "label": "Estado de Calidad Trazable",
            "fieldtype": "Select",
            "options": "Draft\nApproved\nRejected\nCancelled",
            "insert_after": "disabled",
            "read_only": 1
        }).insert(ignore_permissions=True)

def create_sample_workspaces():
    frappe.logger().info("Workspace Smart Quality inicializado.")
