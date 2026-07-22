# Frappe Smart Inventory & Quality Suite (v1.2.0)
> Custom App modular para **Frappe / ERPNext** (v14/v15) enfocada en la gestión de trazabilidad de lotes, inspección de calidad en recepciones de almacén (Purchase Receipt / Stock Entry) y analítica de mermas.

[![Frappe Framework](https://img.shields.io/badge/Frappe-v14%20%2F%20v15-blue.svg)](https://frappeframework.com)
[![ERPNext Compatible](https://img.shields.io/badge/ERPNext-Compatible-green.svg)](https://erpnext.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Descripción General

En cadenas de suministro complejas e industrias sujetas a normativas estricta (alimentaria, farmacéutica, manufactura e insumos), el control de calidad en la entrada de almacén (*Receiving Inspection*) y la trazabilidad de lotes defectuosos son indispensables.

Esta **Custom App** extiende los módulos nativos de ERPNext (`Stock` y `Manufacturing`) mediante:
1. **Inventory Quality Inspection (DocType Personalizado)**: Registro multivariable de inspección de lotes con cálculo de porcentaje de tolerancia/merma y aprobación condicionada de supervisor.
2. **Event Interception via `hooks.py`**: Intercepción de eventos nativos (`Stock Entry`, `Purchase Receipt`) para bloquear automáticamente el consumo de lotes no certificados o rechazados.
3. **Script Report Avanzado (`batch_defect_analytics`)**: Reporte analítico con filtros dinámicos, cálculo de métricas de calidad en SQL y gráficos nativos de Frappe Charts.
4. **API Rest Whitelisted (`external_wms_api.py`)**: Endpoints seguros para integración bidireccional con lectores de código de barras handhelds o sistemas WMS externos.
5. **Print Format Jinja2 (`quality_inspection_certificate.html`)**: Plantilla HTML/CSS responsiva para generación de certificados de calidad en PDF.

---

## 🛠️ Arquitectura de la App

```text
frappe_smart_inventory/
├── README.md
├── hooks.py                             # Hooks de integración con ERPNext nativo
├── frappe_smart_inventory/
│   ├── api/
│   │   └── external_wms_api.py          # REST API Whitelisted para escáneres/WMS
│   ├── doctype/
│   │   └── inventory_quality_inspection/# DocType personalizado con controladores Python y JS
│   │       ├── inventory_quality_inspection.json
│   │       ├── inventory_quality_inspection.py
│   │       └── inventory_quality_inspection.js
│   ├── public/
│   │   └── js/
│   │       └── stock_entry_custom.js    # Inyección JS en formularios nativos
│   ├── reports/
│   │   └── batch_defect_analytics/      # Script Report analítico (Python + SQL + Charts)
│   │       ├── batch_defect_analytics.py
│   │       └── batch_defect_analytics.js
│   └── templates/
│       └── print_formats/
│           └── quality_inspection_certificate.html # Plantilla Jinja2 / PDF
```

---

## 💻 Instalación en Entorno Bench

```bash
# 1. Clonar o descargar la app en el entorno bench
bench get-app https://github.com/TU-USUARIO/frappe_smart_inventory.git

# 2. Instalar la app en tu sitio de ERPNext
bench --site tu-sitio.local install-app frappe_smart_inventory

# 3. Migrar la base de datos
bench --site tu-sitio.local migrate
```

---

## 🧪 Pruebas Unitarias

```bash
bench run-tests --app frappe_smart_inventory
```

---

## 📄 Licencia
Este proyecto está publicado bajo la Licencia MIT.
