# -*- coding: utf-8 -*-
{
    "name": "GCC Project Invoice (Advance, Retention, Deductions)",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Project invoicing with advance payment deduction, retention, performance bond and penalties",
    "description": """
        Extends customer invoices with:
        - Contract/PO/Invoice references
        - Project-based invoicing with down payment management
        - Advance payment deduction (dedicated account, not reserve)
        - Penalties & deductions
        - Performance bond
        - Retention %
        - Automated down payment tracking and reconciliation
        - Project financial monitoring and reporting
        Creates extra journal lines on post to split receivable (receivable, retention receivable, performance bond, advance, deductions).
    """,
    "author": "GCC",
    "license": "LGPL-3",
    "depends": ["account", "project", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/res_config_settings_views.xml",
        "views/project_project_views.xml",
        "views/project_down_payment_views.xml",
    ],
    "installable": True,
    "application": False,
}
