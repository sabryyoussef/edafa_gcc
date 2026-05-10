#!/bin/bash
# Stop Odoo for this project

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$PROJECT_DIR/.odoo.pid"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [ ! -f "$PID_FILE" ]; then
    print_error "PID file not found. Odoo may not be running."
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! kill -0 "$PID" 2>/dev/null; then
    print_error "Process $PID is not running."
    rm -f "$PID_FILE"
    exit 1
fi

print_info "Stopping Odoo (PID: $PID)..."
kill "$PID"

# Wait for process to stop
for i in {1..10}; do
    if ! kill -0 "$PID" 2>/dev/null; then
        break
    fi
    sleep 1
done

if kill -0 "$PID" 2>/dev/null; then
    print_error "Process did not stop, forcing kill..."
    kill -9 "$PID"
fi

rm -f "$PID_FILE"
print_info "Odoo stopped successfully."

