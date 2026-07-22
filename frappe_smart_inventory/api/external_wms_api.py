import frappe
from frappe import _
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=False)
def sync_wms_inspection(batch_no, item_code, sample_size, inspector_email, defects=None):
    """
    Endpoint API REST RESTful para integración con sistemas WMS / Handhelds
    POST /api/method/frappe_smart_inventory.api.external_wms_api.sync_wms_inspection
    """
    try:
        doc = frappe.get_doc({
            "doctype": "Inventory Quality Inspection",
            "inspection_date": nowdate(),
            "inspector": inspector_email,
            "item_code": item_code,
            "batch_no": batch_no,
            "sample_size": float(sample_size)
        })
        
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "inspection_id": doc.name,
            "result": doc.inspection_result,
            "message": _("Inspección de WMS registrada correctamente.")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WMS Sync Quality Error")
        return {
            "status": "error",
            "message": str(e)
        }

def cleanup_expired_draft_inspections():
    """Cron ejecutado diariamente vía scheduler_events"""
    frappe.logger().info("Ejecutando limpieza de inspecciones en borrador inactivas...")
