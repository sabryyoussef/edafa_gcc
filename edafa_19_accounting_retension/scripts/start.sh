#!/bin/bash
# Start Odoo for this project
# Usage: ./scripts/start.sh [--workers <num>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# Go up 2 levels: projects/edafa_19_accounting_retension -> projects -> base_odoo_19
BASE_DIR="$(cd "$PROJECT_DIR/../.." && pwd)"
CONFIG_FILE="$PROJECT_DIR/config/odoo.conf"
ODOO_BIN="$BASE_DIR/odoo19/odoo19/odoo-bin"
VENV_PATH="$PROJECT_DIR/venv"
# Fallback to master venv if project venv doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    VENV_PATH="$BASE_DIR/venv19"
    print_warn "Project venv not found, using master venv. Run: $BASE_DIR/scripts/setup_project_venv.sh $(basename "$PROJECT_DIR")"
fi

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Config file not found: $CONFIG_FILE"
    exit 1
fi

# Get port from config
HTTP_PORT=$(grep "^http_port" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ' || echo "8019")
DB_NAME=$(grep "^db_name" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ' || echo "")

# Parse arguments
WORKERS=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    print_error "Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Check if already running
PID_FILE="$PROJECT_DIR/.odoo.pid"
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    print_warn "Odoo appears to be already running (PID: $(cat "$PID_FILE"))"
    read -p "Do you want to stop it and start a new instance? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        "$PROJECT_DIR/scripts/stop.sh"
        sleep 2
    else
        exit 0
    fi
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Build command
CMD="python3 $ODOO_BIN -c $CONFIG_FILE"

if [ -n "$WORKERS" ]; then
    CMD="$CMD --workers=$WORKERS"
fi

print_info "Starting Odoo..."
print_info "Project: $(basename "$PROJECT_DIR")"
print_info "Database: $DB_NAME"
print_info "Port: $HTTP_PORT"
print_info "Config: $CONFIG_FILE"
print_info ""
print_info "Access at: http://localhost:$HTTP_PORT"
print_info "Press Ctrl+C to stop"

# Start Odoo in background and save PID
nohup $CMD > "$PROJECT_DIR/logs/startup.log" 2>&1 &
echo $! > "$PID_FILE"

print_info "Odoo started with PID: $(cat "$PID_FILE")"
print_info "Logs: tail -f $PROJECT_DIR/logs/odoo.log"
