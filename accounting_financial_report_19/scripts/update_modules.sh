#!/bin/bash
# Update Odoo modules for this project
# Usage: ./scripts/update_modules.sh [module1,module2,...] [--all]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# Go up 2 levels: projects/accounting_financial_report_19 -> projects -> base_odoo_19
BASE_DIR="$(cd "$PROJECT_DIR/../.." && pwd)"
CONFIG_FILE="$PROJECT_DIR/config/odoo.conf"
ODOO_BIN="$BASE_DIR/odoo19/odoo19/odoo-bin"
VENV_PATH="$PROJECT_DIR/venv"
# Fallback to master venv if project venv doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    VENV_PATH="$BASE_DIR/venv19"
    print_warn "Project venv not found, using master venv. Run: $BASE_DIR/scripts/setup_project_venv.sh $(basename "$PROJECT_DIR")"
fi

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Config file not found: $CONFIG_FILE"
    exit 1
fi

DB_NAME=$(grep "^db_name" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ' || echo "")

if [ -z "$DB_NAME" ]; then
    print_error "Database name not found in config"
    exit 1
fi

source "$VENV_PATH/bin/activate"

if [ "$1" == "--all" ]; then
    print_info "Updating all modules..."
    python3 "$ODOO_BIN" -c "$CONFIG_FILE" -d "$DB_NAME" -u all --stop-after-init
elif [ -n "$1" ]; then
    print_info "Updating modules: $1"
    python3 "$ODOO_BIN" -c "$CONFIG_FILE" -d "$DB_NAME" -u "$1" --stop-after-init
else
    print_error "Specify modules to update or use --all"
    echo "Usage: $0 [module1,module2,...] [--all]"
    exit 1
fi

print_info "Modules updated successfully!"

