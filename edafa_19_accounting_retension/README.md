# Edafa 19 Accounting Retention Project

## Project Information

- **Project Name:** edafa_19_accounting_retension
- **Database:** edafa_19_accounting_retension_dev
- **Port:** 8020
- **URL:** http://localhost:8020

## Custom Modules

This project includes the following custom modules:

1. **custom_document_reports** - Custom document reports
2. **payment_fee_calculator** - Payment fee calculation
3. **payment_fee_calculator_19** - Payment fee calculator for Odoo 19
4. **pdf_extracted_content** - PDF content extraction

## Quick Start

```bash
# Start Odoo
./scripts/start.sh

# Stop Odoo
./scripts/stop.sh

# Update modules
./scripts/update_modules.sh

# Install modules
./scripts/install_modules.sh
```

## Access

- **Web Interface:** http://localhost:8020
- **Database:** edafa_19_accounting_retension_dev
- **Logs:** logs/odoo.log

## Project Structure

```
edafa_19_accounting_retension/
├── config/
│   └── odoo.conf          # Project configuration
├── scripts/
│   ├── start.sh           # Start Odoo
│   ├── stop.sh            # Stop Odoo
│   ├── update_modules.sh  # Update modules
│   └── install_modules.sh # Install modules
├── custom_addons/         # Custom modules
├── data/                  # Data files
└── logs/                  # Log files
```

## Notes

This project is self-contained and can be easily archived or moved.
