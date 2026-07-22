frappe.ui.form.on('Inventory Quality Inspection', {
    refresh: function(frm) {
        set_indicator_status(frm);

        if (frm.doc.docstatus === 1 && frm.doc.status !== 'Rejected') {
            frm.add_custom_button(__('Imprimir Certificado'), function() {
                var w = window.open(
                    frappe.urllib.get_full_url(
                        "/api/method/frappe.utils.print_format.download_pdf?"
                        + "doctype=" + encodeURIComponent(frm.doc.doctype)
                        + "&name=" + encodeURIComponent(frm.doc.name)
                        + "&format=Quality%20Inspection%20Certificate"
                        + "&no_letterhead=0"
                    )
                );
                if (!w) {
                    frappe.msgprint(__('Habilite las ventanas emergentes.'));
                }
            }, __('Impresión'));

            frm.add_custom_button(__('Ver Lote en ERPNext'), function() {
                if (frm.doc.batch_no) {
                    frappe.set_route('Form', 'Batch', frm.doc.batch_no);
                }
            }, __('Inventario'));
        }

        if (frm.doc.inspection_result === 'Rejected' && frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Autorizar Excepción'), function() {
                frappe.prompt([
                    {
                        fieldname: 'reason',
                        fieldtype: 'Small Text',
                        label: 'Motivo de Excepción',
                        reqd: 1
                    }
                ], function(values) {
                    frm.set_value('supervisor_override', 1);
                    frm.set_value('override_reason', values.reason);
                    frm.save();
                    frappe.show_alert({message: __('Excepción registrada'), indicator: 'green'});
                }, __('Autorizar Lote Fuera de Norma'), __('Confirmar'));
            }).addClass('btn-danger');
        }
    },

    sample_size: function(frm) {
        recalculate_totals(frm);
    }
});

frappe.ui.form.on('Inventory Quality Defect Item', {
    quantity: function(frm, cdt, cdn) {
        recalculate_totals(frm);
    },
    defect_items_remove: function(frm) {
        recalculate_totals(frm);
    }
});

function recalculate_totals(frm) {
    let total_defects = 0.0;
    (frm.doc.defect_items || []).forEach(row => {
        total_defects += flt(row.quantity);
    });

    let sample = flt(frm.doc.sample_size);
    let accepted = sample - total_defects;
    let rate = sample > 0 ? (total_defects / sample) * 100 : 0;

    frm.set_value('defective_units', total_defects);
    frm.set_value('accepted_units', accepted > 0 ? accepted : 0);
    frm.set_value('defect_percentage', flt(rate, 2));

    let result = "Passed - Grade A";
    if (rate > 10) result = "Rejected";
    else if (rate > 5) result = "Conditional Accept";
    else if (rate > 2) result = "Passed - Grade B";

    frm.set_value('inspection_result', result);
}

function set_indicator_status(frm) {
    if (frm.doc.inspection_result && frm.doc.inspection_result.includes('Passed')) {
        frm.page.set_indicator(__(frm.doc.inspection_result), 'green');
    } else if (frm.doc.inspection_result === 'Rejected') {
        frm.page.set_indicator(__('Rechazado'), 'red');
    } else {
        frm.page.set_indicator(__(frm.doc.inspection_result || 'Borrador'), 'orange');
    }
}
