# -*- coding: utf-8 -*-
{
    'name': 'Payment Method Fee Calculator',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Calculate payment fees for Mada and Visa/Mastercard payment methods',
    'description': """
Payment Method Fee Calculator
=============================
This module adds configurable fee calculation for payment methods:

* Mada: Tiered fee structure
  - Amount < 5,000 SAR: 0.8% of transaction amount
  - Amount >= 5,000 SAR: Fixed 40 SAR

* Visa/Mastercard: Flat rate
  - All amounts: 2.5% of transaction amount

All fee rates and thresholds are configurable in the journal settings.
Fees are calculated exclusive of VAT.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
    ],
    'demo': [
        'demo/account_journal_demo.xml',
        'demo/account_payment_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

