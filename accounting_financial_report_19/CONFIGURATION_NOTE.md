# Configuration Note: Custom Addons Path

## Current Status

The `custom_addons` directory is **NOT** currently added to the Odoo configuration `addons_path`. This is intentional to avoid conflicts.

## Why?

1. **Mixed Versions**: The `custom_addons` directory contains modules at different Odoo versions:
   - ✅ `date_range`: **19.0.1.0.0** (migrated)
   - ❌ `account_financial_report`: **18.0.1.4.2** (not migrated)
   - ❌ `report_xlsx`: **18.0.1.1.2** (not migrated)

2. **Conflict Prevention**: Loading Odoo 18 modules in an Odoo 19 instance can cause:
   - Database schema conflicts
   - Runtime errors
   - Module installation failures
   - Data integrity issues

3. **Other Projects**: The master config includes other projects' `custom_addons` paths that may contain Odoo 18 modules.

## Current Configuration

**File**: `config/odoo.conf`

```ini
addons_path = /home/sabry3/sabry_backup/odoo_base/base_odoo_19/odoo19/odoo19/addons
```

**Note**: This explicitly overrides the master config to avoid loading other projects' custom_addons.

## When to Add Custom Addons Path

Add the `custom_addons` path **ONLY AFTER** all modules in this project are migrated to Odoo 19.0:

```ini
addons_path = /home/sabry3/sabry_backup/odoo_base/base_odoo_19/odoo19/odoo19/addons,/home/sabry3/sabry_backup/odoo_base/base_odoo_19/projects/accounting_financial_report_19/custom_addons
```

## Migration Checklist

Before adding `custom_addons` to the config:

- [ ] All modules in `custom_addons/` are migrated to version 19.0.x.x.x
- [ ] All modules have been tested in Odoo 19
- [ ] All dependencies are available in Odoo 19
- [ ] Database migration has been tested (if upgrading existing database)

## Testing Migration Status

To check which modules still need migration:

```bash
grep -r '"version".*"18\.0' custom_addons/*/__manifest__.py
```

All results should be resolved before adding `custom_addons` to `addons_path`.

## Safety

- ✅ Project-specific config ensures isolation from other projects
- ✅ Explicit addons_path prevents accidental loading of Odoo 18 modules
- ✅ Source control (Git) allows rollback if needed
- ⚠️ Never add `custom_addons` until ALL modules are 19.0.x.x.x

