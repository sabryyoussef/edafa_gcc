#!/bin/bash
# Comprehensive system cleanup and compression script
# This script performs safe cleanup and compression operations

set -e

echo "=== System Cleanup and Compression Script ==="
echo ""

# Function to format bytes
format_size() {
    numfmt --to=iec-i --suffix=B "$1" 2>/dev/null || echo "$1 bytes"
}

# Function to get directory size
get_dir_size() {
    du -sb "$1" 2>/dev/null | cut -f1 || echo "0"
}

TOTAL_SAVED=0

# 1. Clean APT cache
echo "1. Cleaning APT package cache..."
APT_CACHE_SIZE=$(get_dir_size /var/cache/apt)
if [ "$APT_CACHE_SIZE" -gt 0 ]; then
    echo "   Current APT cache size: $(format_size $APT_CACHE_SIZE)"
    if sudo apt-get clean 2>/dev/null; then
        NEW_APT_SIZE=$(get_dir_size /var/cache/apt)
        APT_SAVED=$((APT_CACHE_SIZE - NEW_APT_SIZE))
        TOTAL_SAVED=$((TOTAL_SAVED + APT_SAVED))
        echo "   ✓ Cleaned: $(format_size $APT_SAVED)"
    else
        echo "   ✗ Failed (may require sudo)"
    fi
else
    echo "   APT cache already clean"
fi
echo ""

# 2. Compress old log files
echo "2. Compressing old log files..."
if [ -f "$(dirname "$0")/compress_logs.sh" ]; then
    LOG_SAVED=$(bash "$(dirname "$0")/compress_logs.sh" 2>&1 | grep "Total space saved" | grep -oE '[0-9]+[KMGT]?i?B' | head -1)
    echo "   ✓ Log compression completed"
else
    echo "   ⚠ compress_logs.sh not found, skipping"
fi
echo ""

# 3. Clean temporary files older than 7 days
echo "3. Cleaning old temporary files..."
TMP_DIRS=("/tmp" "/var/tmp")
for tmp_dir in "${TMP_DIRS[@]}"; do
    if [ -d "$tmp_dir" ]; then
        TMP_SIZE_BEFORE=$(get_dir_size "$tmp_dir")
        echo "   Cleaning $tmp_dir..."
        # Find and remove files older than 7 days (safe operation)
        find "$tmp_dir" -type f -mtime +7 -delete 2>/dev/null || true
        find "$tmp_dir" -type d -empty -mtime +7 -delete 2>/dev/null || true
        TMP_SIZE_AFTER=$(get_dir_size "$tmp_dir")
        TMP_SAVED=$((TMP_SIZE_BEFORE - TMP_SIZE_AFTER))
        if [ "$TMP_SAVED" -gt 0 ]; then
            TOTAL_SAVED=$((TOTAL_SAVED + TMP_SAVED))
            echo "   ✓ Cleaned $tmp_dir: $(format_size $TMP_SAVED)"
        fi
    fi
done
echo ""

# 4. Report journal compression status
echo "4. Checking systemd journal compression..."
if grep -q "^Compress=yes" /etc/systemd/journald.conf 2>/dev/null; then
    echo "   ✓ Journal compression is enabled"
    echo "   New journal entries will be automatically compressed"
else
    echo "   ⚠ Journal compression not enabled in journald.conf"
fi
echo ""

# Summary
echo "=== Cleanup Summary ==="
echo "Total space freed: $(format_size $TOTAL_SAVED)"
echo ""
echo "Note: Some operations may require sudo privileges."
echo "Run with sudo for full functionality."

