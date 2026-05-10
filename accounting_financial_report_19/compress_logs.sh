#!/bin/bash
# Script to compress uncompressed log files in /var/log
# This script compresses old log files that are not already compressed

set -e

LOG_DIR="/var/log"
COMPRESSED_EXTENSIONS=".gz .bz2 .xz .zst"
TOTAL_SAVED=0

echo "=== Log File Compression Script ==="
echo "Starting compression of uncompressed log files..."
echo ""

# Function to get file size in bytes
get_size() {
    du -b "$1" 2>/dev/null | cut -f1
}

# Function to compress file and report savings
compress_file() {
    local file="$1"
    local original_size=$(get_size "$file")
    
    if [ -z "$original_size" ] || [ "$original_size" -eq 0 ]; then
        return
    fi
    
    echo "Compressing: $file ($(numfmt --to=iec-i --suffix=B $original_size))"
    
    # Use gzip for compatibility (most common)
    if gzip -f "$file" 2>/dev/null; then
        local compressed_size=$(get_size "${file}.gz")
        local saved=$((original_size - compressed_size))
        TOTAL_SAVED=$((TOTAL_SAVED + saved))
        echo "  ✓ Saved: $(numfmt --to=iec-i --suffix=B $saved) ($(echo "scale=1; $saved*100/$original_size" | bc)%)"
    else
        echo "  ✗ Failed to compress"
    fi
}

# Find and compress uncompressed log files
# Target: rotated logs (.1, .2, etc.) and old logs that aren't compressed
# Use process substitution to avoid subshell issues
while IFS= read -r file; do
    compress_file "$file"
done < <(find "$LOG_DIR" -type f \( \
    -name "*.log.[0-9]*" \
    -o -name "*.log.[0-9][0-9]*" \
    -o -name "*.log.old" \
\) ! -name "*.gz" ! -name "*.bz2" ! -name "*.xz" ! -name "*.zst" \
-size +100k -mtime +1)

# Also compress large uncompressed log files older than 1 day
while IFS= read -r file; do
    # Skip active system logs
    if [[ "$file" =~ (syslog|auth\.log|kern\.log)$ ]] && [ "$(stat -c %Y "$file" 2>/dev/null)" -gt "$(date -d '1 day ago' +%s)" ]; then
        continue
    fi
    compress_file "$file"
done < <(find "$LOG_DIR" -type f -name "*.log" ! -name "*.gz" ! -name "*.bz2" ! -name "*.xz" ! -name "*.zst" \
-size +1M -mtime +7)

echo ""
echo "=== Compression Complete ==="
if [ "$TOTAL_SAVED" -gt 0 ]; then
    echo "Total space saved: $(numfmt --to=iec-i --suffix=B $TOTAL_SAVED)"
else
    echo "Total space saved: Calculated during compression (see above)"
fi
echo ""
echo "Note: Active log files were not compressed to avoid disrupting services."

