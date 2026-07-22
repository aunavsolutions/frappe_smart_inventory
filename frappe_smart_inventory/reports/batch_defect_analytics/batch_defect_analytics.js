frappe.query_reports["Batch Defect Analytics"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("Desde"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("Hasta"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "supplier",
            "label": __("Proveedor"),
            "fieldtype": "Link",
            "options": "Supplier"
        },
        {
            "fieldname": "inspection_result",
            "label": __("Dictamen"),
            "fieldtype": "Select",
            "options": "\nPassed - Grade A\nPassed - Grade B\nConditional Accept\nRejected"
        }
    ]
};
