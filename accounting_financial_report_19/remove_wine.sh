#!/bin/bash
# Script to remove Wine and all Wine-related packages
# Wine is used to run Windows applications on Linux

set -e

echo "=== Wine Package Removal Script ==="
echo ""

# Find all Wine packages
WINE_PACKAGES=$(dpkg -l | grep -E "^ii.*wine" | awk '{print $2}')

if [ -z "$WINE_PACKAGES" ]; then
    echo "✓ No Wine packages found"
    exit 0
fi

echo "Wine packages to remove:"
TOTAL_SIZE=0
echo "$WINE_PACKAGES" | while read pkg; do
    size=$(dpkg-query -Wf '${Installed-Size}\t${Package}\n' "$pkg" 2>/dev/null | awk '{printf "%.1f", $1/1024}')
    echo "  - $pkg (${size} MB)"
done

TOTAL_SIZE=$(dpkg-query -Wf '${Installed-Size}\t${Package}\n' | grep -E "(wine|libwine)" | awk '{sum+=$1} END {printf "%.1f", sum/1024}')
echo ""
echo "Total size: ${TOTAL_SIZE} MB (~$(echo "$TOTAL_SIZE/1024" | bc -l | awk '{printf "%.2f", $1}') GB)"
echo ""

# Remove Wine packages
echo "Removing Wine packages..."
echo "$WINE_PACKAGES" | xargs sudo apt-get remove --purge -y

# Clean up any dependencies
echo ""
echo "Cleaning up unused dependencies..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo ""
echo "=== Wine Removal Complete ==="
echo ""
echo "✓ All Wine packages have been removed"

