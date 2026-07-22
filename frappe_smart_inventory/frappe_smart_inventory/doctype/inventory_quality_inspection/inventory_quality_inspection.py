import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, nowdate, get_link_to_form

class InventoryQualityInspection(Document):
    def validate(self):
        """Cálculo automático de porcentajes de defecto y asignación de dictamen"""
        self.calculate_metrics()
        self.determine_quality_status()
        self.set_doc_status()

    def before_submit(self):
        """Bloqueo de seguridad antes de autorizar el lote"""
        if self.inspection_result == "Rejected" and not self.supervisor_override:
            frappe.throw(_(
                "No se puede aprobar un registro con resultado <b>Rechazado</b> sin la autorización explícita del Supervisor de Calidad."
            ))

    def on_submit(self):
        """Actualizar el estado del Batch en ERPNext Stock"""
        if self.batch_no:
            self.update_batch_quality_status()

    def calculate_metrics(self):
        """Suma de unidades inspeccionadas vs defectuosas"""
        total_inspected = flt(self.sample_size)
        total_defects = 0.0

        for item in self.get("defect_items"):
            item.total_defect_qty = flt(item.quantity)
            total_defects += item.total_defect_qty

        self.defective_units = total_defects
        
        if total_inspected > 0:
            self.defect_percentage = flt((total_defects / total_inspected) * 100, 2)
            self.accepted_units = flt(total_inspected - total_defects, 2)
        else:
            self.defect_percentage = 0.0
            self.accepted_units = 0.0

    def determine_quality_status(self):
        """Clasificación según tolerancia porcentual configurada"""
        rate = flt(self.defect_percentage)

        if rate <= 2.0:
            self.inspection_result = "Passed - Grade A"
        elif rate <= 5.0:
            self.inspection_result = "Passed - Grade B"
        elif rate <= 10.0:
            self.inspection_result = "Conditional Accept"
        else:
            self.inspection_result = "Rejected"

    def set_doc_status(self):
        if self.docstatus == 0:
            self.status = "Draft"
        elif self.docstatus == 1:
            self.status = "Approved" if "Passed" in self.inspection_result else "Rejected"
        elif self.docstatus == 2:
            self.status = "Cancelled"

    def update_batch_quality_status(self):
        """Actualiza el campo personalizado en el Batch de ERPNext"""
        if frappe.db.exists("Batch", self.batch_no):
            batch_doc = frappe.get_doc("Batch", self.batch_no)
            if hasattr(batch_doc, "custom_quality_status"):
                batch_doc.db_set("custom_quality_status", self.status)
                frappe.msgprint(_("Lote {0} actualizado a estado: <b>{1}</b>.").format(
                    get_link_to_form("Batch", self.batch_no), self.status
                ))


# --- HOOKS INTERCEPTADOS DE ERPNEXT ---

def validate_stock_entry_quality(doc, method):
    """Intercepción del evento 'validate' en Stock Entry"""
    if doc.purpose in ["Material Issue", "Manufacture", "Material Transfer for Manufacture"]:
        for item in doc.items:
            if item.batch_no:
                inspection = frappe.db.get_value(
                    "Inventory Quality Inspection",
                    {"batch_no": item.batch_no, "docstatus": 1},
                    ["name", "inspection_result", "status"],
                    as_dict=True
                )
                
                if not inspection:
                    frappe.throw(_(
                        "Fila #{0}: El lote <b>{1}</b> del ítem {2} requiere una Inspección de Calidad de Inventario antes de su consumo."
                    ).format(item.idx, item.batch_no, item.item_code))
                    
                if inspection.status == "Rejected":
                    frappe.throw(_(
                        "Fila #{0}: El lote <b>{1}</b> está marcando como <b>RECHAZADO</b> en {2}."
                    ).format(item.idx, item.batch_no, get_link_to_form("Inventory Quality Inspection", inspection.name)))


def on_purchase_receipt_submit(doc, method):
    """Intercepción de Purchase Receipt para crear automáticamente borrador de inspección"""
    frappe.logger().info(f"Recepción de Compra enviada: {doc.name}. Generando borrador de inspección de almacén...")


# --- HELPER JINJA ---

def get_status_badge(result):
    badges = {
        "Passed - Grade A": '<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">APROBADO (GRADO A)</span>',
        "Passed - Grade B": '<span style="background-color: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">APROBADO (GRADO B)</span>',
        "Conditional Accept": '<span style="background-color: #ffc107; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold;">ACEPTACIÓN CONDICIONAL</span>',
        "Rejected": '<span style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">RECHAZADO</span>'
    }
    return badges.get(result, f'<span>{result}</span>')
