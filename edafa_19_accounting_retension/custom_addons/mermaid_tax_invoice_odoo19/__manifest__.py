{
    "name": "Mermaid Tax Invoice (Odoo 19)",
    "version": "19.0.1.0.0",
    "category": "Accounting/Reports",
    "summary": "Tax invoice layout identical to provided screenshot.",
    "depends": ["account", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
        "report/report.xml",
        "views/report_tax_invoice.xml"
    ],
    "demo": [
        "demo/account_move_demo.xml",
    ],
    "installable": True,
    "application": False
}