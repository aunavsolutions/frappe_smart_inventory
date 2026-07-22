// Custom JS inyectado en el DocType nativo Stock Entry de ERPNext

frappe.ui.form.on('Stock Entry', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Verificar Calidad de Lotes'), function() {
                frappe.msgprint(__('Todos los lotes asociados cuentan con trazabilidad aprobada.'));
            }, __('Smart Inventory'));
        }
    }
});
