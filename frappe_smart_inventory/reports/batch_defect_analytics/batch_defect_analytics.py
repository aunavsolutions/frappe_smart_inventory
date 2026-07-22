import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    report_summary = get_report_summary(data)
    
    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {
            "fieldname": "inspection_id",
            "label": _("Inspección"),
            "fieldtype": "Link",
            "options": "Inventory Quality Inspection",
            "width": 150
        },
        {
            "fieldname": "inspection_date",
            "label": _("Fecha"),
            "fieldtype": "Date",
            "width": 110
        },
        {
            "fieldname": "supplier",
            "label": _("Proveedor"),
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 160
        },
        {
            "fieldname": "item_code",
            "label": _("Artículo"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        },
        {
            "fieldname": "batch_no",
            "label": _("Lote"),
            "fieldtype": "Link",
            "options": "Batch",
            "width": 130
        },
        {
            "fieldname": "sample_size",
            "label": _("Muestra"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "defective_units",
            "label": _("Defectuosas"),
            "fieldtype": "Float",
            "width": 110
        },
        {
            "fieldname": "defect_percentage",
            "label": _("% Merma"),
            "fieldtype": "Percent",
            "width": 100
        },
        {
            "fieldname": "inspection_result",
            "label": _("Dictamen"),
            "fieldtype": "Data",
            "width": 150
        }
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND inspection_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
    if filters.get("supplier"):
        conditions += f" AND supplier = '{filters.get('supplier')}'"
    if filters.get("inspection_result"):
        conditions += f" AND inspection_result = '{filters.get('inspection_result')}'"

    query = f"""
        SELECT 
            name as inspection_id,
            inspection_date,
            supplier,
            item_code,
            batch_no,
            sample_size,
            defective_units,
            defect_percentage,
            inspection_result
        FROM 
            `tabInventory Quality Inspection`
        WHERE 
            docstatus = 1 {conditions}
        ORDER BY 
            inspection_date DESC
    """
    return frappe.db.sql(query, as_dict=True)

def get_chart_data(data):
    if not data:
        return None
        
    suppliers = {}
    for row in data:
        supp = row.supplier or "Sin Proveedor"
        suppliers[supp] = suppliers.get(supp, 0) + row.defective_units

    return {
        "data": {
            "labels": list(suppliers.keys()),
            "datasets": [{"name": _("Unidades Defectuosas"), "values": list(suppliers.values())}]
        },
        "type": "bar",
        "colors": ["#e74c3c"]
    }

def get_report_summary(data):
    if not data:
        return []
        
    total_sample = sum(row.sample_size for row in data)
    total_defects = sum(row.defective_units for row in data)
    avg_defect = (total_defects / total_sample * 100) if total_sample > 0 else 0

    return [
        {
            "value": total_sample,
            "label": _("Total Unidades Inspeccionadas"),
            "datatype": "Float",
            "indicator": "Blue"
        },
        {
            "value": total_defects,
            "label": _("Total Unidades Defectuosas"),
            "datatype": "Float",
            "indicator": "Red"
        },
        {
            "value": avg_defect,
            "label": _("% Tasa Promedio de Merma"),
            "datatype": "Percent",
            "indicator": "Orange"
        }
    ]
