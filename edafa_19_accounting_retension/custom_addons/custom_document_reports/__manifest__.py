# -*- coding: utf-8 -*-
{
    'name': 'Custom Document Reports',
    'version': '19.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Custom Delivery Note, Packing List, Tax Invoice and Commercial Invoice Reports',
    'description': """
Custom Document Reports
========================
This module provides custom report templates based on extracted PDF documents:

* Delivery Note - Custom delivery note format for stock pickings
* Packing List - Bilingual (English/Arabic) packing list with VAT information
* Tax Invoice - Tax invoice with VAT breakdown
* Commercial Invoice - Commercial invoice with L/C details and shipping information

All reports are based on real document formats and include:
- Company and customer information
- Item details with quantities and prices
- VAT information where applicable
- Bilingual support (English/Arabic)
- Signature sections
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['account', 'stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'reports/stock_reports.xml',
        'reports/account_reports.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

