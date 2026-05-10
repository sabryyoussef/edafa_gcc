#!/bin/bash
# Start Odoo for this project
# Usage: ./scripts/start.sh [--workers <num>]

set -e

# Resolve consistent mount paths to prevent path resolution errors
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# Convert to mount path if using symlink/bind mount
PROJECT_DIR="$(readlink -f "$PROJECT_DIR" | sed 's|/home/sabry3/sabry_backup|/mnt/sabry_backup|')"
BASE_DIR="$(readlink -f "$PROJECT_DIR/../.." | sed 's|/home/sabry3/sabry_backup|/mnt/sabry_backup|')"
CONFIG_FILE="$PROJECT_DIR/config/odoo.conf"
ODOO_BIN="$BASE_DIR/odoo19/odoo19/odoo-bin"
VENV_PATH="$PROJECT_DIR/venv"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Always use master venv for now (project venv needs package installation)
VENV_PATH="$BASE_DIR/venv19"
print_info "Using master venv at $VENV_PATH"

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
    print_error "Paths resolved: PROJECT_DIR=$PROJECT_DIR, BASE_DIR=$BASE_DIR"
    exit 1
fi

# Check if Odoo binary exists
if [ ! -f "$ODOO_BIN" ]; then
    print_error "Odoo binary not found at $ODOO_BIN"
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

print_info "Starting Odoo..."
print_info "Project: $(basename "$PROJECT_DIR")"
print_info "Database: $DB_NAME"
print_info "Port: $HTTP_PORT"
print_info "Config: $CONFIG_FILE"
print_info "Python: $VENV_PATH/bin/python"
print_info "Odoo Binary: $ODOO_BIN"
print_info ""
print_info "Access at: http://localhost:$HTTP_PORT"
print_info "Starting in background..."

# Ensure log directory exists
mkdir -p "$PROJECT_DIR/logs"

# Start Odoo in background and save PID with explicit paths
if [ -n "$WORKERS" ]; then
    nohup "$VENV_PATH/bin/python" "$ODOO_BIN" -c "$CONFIG_FILE" --workers="$WORKERS" > "$PROJECT_DIR/logs/startup.log" 2>&1 &
else
    nohup "$VENV_PATH/bin/python" "$ODOO_BIN" -c "$CONFIG_FILE" > "$PROJECT_DIR/logs/startup.log" 2>&1 &
fi
echo $! > "$PID_FILE"

print_info "Odoo started with PID: $(cat "$PID_FILE")"
print_info "Logs: tail -f $PROJECT_DIR/logs/odoo.log"

