# -*- coding: utf-8 -*-
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import nowdate

class TestInventoryQualityInspection(FrappeTestCase):
    def setUp(self):
        """Creación de datos semilla para pruebas unitarias de calidad"""
        self.create_test_dependencies()

    def create_test_dependencies(self):
        # Crear ítem de prueba si no existe
        if not frappe.db.exists("Item", "_Test Raw Material Leather"):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": "_Test Raw Material Leather",
                "item_name": "Cuero Vacuno Test",
                "item_group": "Raw Material",
                "has_batch_no": 1
            })
            item.insert(ignore_permissions=True)

        # Crear Lote de prueba
        if not frappe.db.exists("Batch", "_TEST-BATCH-2026"):
            batch = frappe.get_doc({
                "doctype": "Batch",
                "batch_id": "_TEST-BATCH-2026",
                "item": "_Test Raw Material Leather"
            })
            batch.insert(ignore_permissions=True)

    def test_quality_inspection_calculation_pass(self):
        """Prueba 1: Inspección aprobada (Grado A - Merma < 2%)"""
        doc = frappe.get_doc({
            "doctype": "Inventory Quality Inspection",
            "inspection_date": nowdate(),
            "inspector": "Administrator",
            "item_code": "_Test Raw Material Leather",
            "batch_no": "_TEST-BATCH-2026",
            "sample_size": 100,
            "defect_items": [
                {
                    "defect_type": "Superficial Grain Mark",
                    "quantity": 1
                }
            ]
        })
        doc.insert()
        
        # Aserciones unitarias
        self.assertEqual(doc.defective_units, 1.0)
        self.assertEqual(doc.accepted_units, 99.0)
        self.assertEqual(doc.defect_percentage, 1.0)
        self.assertEqual(doc.inspection_result, "Passed - Grade A")

    def test_quality_inspection_rejection_validation(self):
        """Prueba 2: Intento de aprobación de lote rechazado sin firma de supervisor debe lanzar excepción"""
        doc = frappe.get_doc({
            "doctype": "Inventory Quality Inspection",
            "inspection_date": nowdate(),
            "inspector": "Administrator",
            "item_code": "_Test Raw Material Leather",
            "batch_no": "_TEST-BATCH-2026",
            "sample_size": 100,
            "defect_items": [
                {
                    "defect_type": "Severe Thickness Deviation",
                    "quantity": 25 # 25% merma -> Rechazado
                }
            ]
        })
        doc.insert()
        
        self.assertEqual(doc.inspection_result, "Rejected")
        
        # Validar que frappe.throw es lanzado al intentar hacer submit sin supervisor_override
        self.assertRaises(frappe.ValidationError, doc.submit)
