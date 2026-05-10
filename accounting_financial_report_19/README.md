# Accounting Financial Report 19 Project

## Project Information

- **Project Name:** accounting_financial_report_19
- **Database:** accounting_financial_report_19_dev
- **Port:** 8021
- **URL:** http://localhost:8021

## Custom Modules

This project includes the following custom modules:

1. **account_financial_report** - Comprehensive financial reporting module
   - General Ledger
   - Trial Balance
   - Aged Partner Balance
   - Open Items
   - Journal Ledger
   - VAT Report
   - Excel export support

2. **date_range** - Date range management for reporting periods

3. **report_xlsx** - Excel report generation framework

## Quick Start

```bash
# Start Odoo
./scripts/start.sh

# Stop Odoo
./scripts/stop.sh

# Update modules
./scripts/update_modules.sh --all
# or specific modules
./scripts/update_modules.sh account_financial_report,date_range

# Install modules
./scripts/install_modules.sh account_financial_report,date_range,report_xlsx
```

## Access

- **Web Interface:** http://localhost:8021
- **Database:** accounting_financial_report_19_dev
- **Logs:** logs/odoo.log

## Project Structure

```
accounting_financial_report_19/
├── config/
│   └── odoo.conf          # Project configuration
├── scripts/
│   ├── start.sh           # Start Odoo
│   ├── stop.sh            # Stop Odoo
│   ├── update_modules.sh  # Update modules
│   └── install_modules.sh # Install modules
├── custom_addons/         # Custom modules
│   ├── account_financial_report/
│   ├── date_range/
│   └── report_xlsx/
├── data/                  # Data files
│   ├── demo_data/
│   └── fixtures/
└── logs/                  # Log files
```

## Module Details

### account_financial_report

Provides comprehensive financial reporting capabilities:
- **General Ledger**: Detailed account transactions
- **Trial Balance**: Account balances summary
- **Aged Partner Balance**: Outstanding receivables/payables by age
- **Open Items**: Unreconciled transactions
- **Journal Ledger**: All journal entries
- **VAT Report**: Tax reporting

All reports support:
- PDF export
- Excel export (via report_xlsx)
- Date range filtering
- Custom configurations

### date_range

Manages date ranges for reporting periods:
- Fiscal year periods
- Custom date ranges
- Recurring periods

### report_xlsx

Framework for generating Excel reports:
- XLSX format support
- Template-based reports
- Styling and formatting

## Notes

This project is self-contained and can be easily archived or moved.

For more information about the modules, see:
- `custom_addons/account_financial_report/README.rst`
- `custom_addons/date_range/README.rst`
- `custom_addons/report_xlsx/README.rst`

