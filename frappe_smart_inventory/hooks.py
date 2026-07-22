app_name = "frappe_smart_inventory"
app_title = "Frappe Smart Inventory"
app_publisher = "Antx"
app_description = "Advanced Quality Control & Batch Traceability for ERPNext Stock"
app_email = "dev@example.com"
app_license = "MIT"

# Hooks de Instalación y Configuración Automática
# -----------------------------------------------
after_install = "frappe_smart_inventory.setup.install.after_install"


# Hooks de Documentos en ERPNext Nativo
# ------------------------------------
doc_events = {
    "Stock Entry": {
        "validate": "frappe_smart_inventory.frappe_smart_inventory.doctype.inventory_quality_inspection.inventory_quality_inspection.validate_stock_entry_quality"
    },
    "Purchase Receipt": {
        "on_submit": "frappe_smart_inventory.frappe_smart_inventory.doctype.inventory_quality_inspection.inventory_quality_inspection.on_purchase_receipt_submit"
    }
}

# Inclusión de JS en Formularios Nativo
# ------------------------------------
doctype_js = {
    "Stock Entry": "public/js/stock_entry_custom.js"
}

# Tareas Programadas (Scheduler)
# ------------------------------
scheduler_events = {
    "daily": [
        "frappe_smart_inventory.api.external_wms_api.cleanup_expired_draft_inspections"
    ]
}

# Métodos Jinja Personalizados
# -----------------------------
jinja = {
    "methods": [
        "frappe_smart_inventory.frappe_smart_inventory.doctype.inventory_quality_inspection.inventory_quality_inspection.get_status_badge"
    ]
}
