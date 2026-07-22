import frappe

def execute():
    """Patch de migración ejecutable con 'bench migrate'"""
    frappe.reload_doc("frappe_smart_inventory", "doctype", "inventory_quality_inspection")
    
    # Recalcular porcentajes para datos preexistentes si aplica
    inspections = frappe.get_all("Inventory Quality Inspection", fields=["name", "sample_size", "defective_units"])
    for insp in inspections:
        if insp.sample_size and insp.sample_size > 0:
            rate = (insp.defective_units / insp.sample_size) * 100
            frappe.db.set_value("Inventory Quality Inspection", insp.name, "defect_percentage", rate)
            
    frappe.db.commit()
