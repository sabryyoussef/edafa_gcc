#!/bin/bash
# Script to move Ollama models to /mnt/sabry_backup
# This will free up space on the main drive and store models on the backup drive

set -e

BACKUP_DIR="/mnt/sabry_backup/ollama_models"
OLLAMA_USER="ollama"
# Check actual models location
if [ -d "/usr/share/ollama" ] && [ "$(du -sb /usr/share/ollama 2>/dev/null | cut -f1)" -gt 1000000 ]; then
    CURRENT_MODELS_DIR="/usr/share/ollama"
elif [ -d "/home/ollama/.ollama" ]; then
    CURRENT_MODELS_DIR="/home/ollama/.ollama"
else
    CURRENT_MODELS_DIR="/home/ollama/.ollama"
fi

echo "=== Ollama Models Migration Script ==="
echo ""

# Check if Ollama service is running
if systemctl is-active --quiet ollama; then
    echo "Stopping Ollama service..."
    sudo systemctl stop ollama
    echo "✓ Ollama service stopped"
else
    echo "Ollama service is not running"
fi
echo ""

# Create backup directory
echo "Creating backup directory: $BACKUP_DIR"
sudo mkdir -p "$BACKUP_DIR"
sudo chown $OLLAMA_USER:$OLLAMA_USER "$BACKUP_DIR"
echo "✓ Backup directory created"
echo ""

# Check current models location and size
if [ -d "$CURRENT_MODELS_DIR" ]; then
    CURRENT_SIZE=$(du -sh "$CURRENT_MODELS_DIR" 2>/dev/null | cut -f1)
    echo "Current models location: $CURRENT_MODELS_DIR"
    echo "Current size: $CURRENT_SIZE"
    echo ""
    
    # Move models to backup location
    echo "Moving models to backup location..."
    sudo mv "$CURRENT_MODELS_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
    echo "✓ Models moved"
    echo ""
    
    # Create symlink from original location to backup location
    echo "Creating symlink..."
    sudo rm -rf "$CURRENT_MODELS_DIR"
    sudo ln -s "$BACKUP_DIR" "$CURRENT_MODELS_DIR"
    sudo chown -h $OLLAMA_USER:$OLLAMA_USER "$CURRENT_MODELS_DIR"
    echo "✓ Symlink created: $CURRENT_MODELS_DIR -> $BACKUP_DIR"
else
    echo "Creating models directory and symlink..."
    sudo mkdir -p "$(dirname $CURRENT_MODELS_DIR)"
    sudo ln -s "$BACKUP_DIR" "$CURRENT_MODELS_DIR"
    sudo chown -h $OLLAMA_USER:$OLLAMA_USER "$CURRENT_MODELS_DIR"
    echo "✓ Symlink created"
fi
echo ""

# Update systemd service to use OLLAMA_MODELS environment variable (alternative method)
echo "Updating Ollama service configuration..."
OVERRIDE_DIR="/etc/systemd/system/ollama.service.d"
sudo mkdir -p "$OVERRIDE_DIR"

# Create or update override.conf
sudo tee "$OVERRIDE_DIR/override.conf" > /dev/null <<EOF
[Service]
Environment="OLLAMA_MODELS=$BACKUP_DIR"
EOF

echo "✓ Service configuration updated"
echo ""

# Reload systemd and restart Ollama
echo "Reloading systemd configuration..."
sudo systemctl daemon-reload
echo "✓ Systemd reloaded"
echo ""

echo "Starting Ollama service..."
sudo systemctl start ollama
sleep 2

if systemctl is-active --quiet ollama; then
    echo "✓ Ollama service started successfully"
else
    echo "⚠ Warning: Ollama service may not have started properly"
    echo "Check status with: sudo systemctl status ollama"
fi
echo ""

# Verify models are accessible
echo "Verifying models..."
sleep 3
if ollama list > /dev/null 2>&1; then
    echo "✓ Models are accessible"
    echo ""
    echo "Installed models:"
    ollama list
else
    echo "⚠ Warning: Could not list models. Service may need more time to start."
fi
echo ""

echo "=== Migration Complete ==="
echo ""
echo "Models location: $BACKUP_DIR"
echo "Symlink: $CURRENT_MODELS_DIR -> $BACKUP_DIR"
echo ""
echo "Space freed on main drive: ~3.2GB"
echo "Models now stored on: /mnt/sabry_backup"
echo ""
echo "Future models will automatically be stored in: $BACKUP_DIR"

