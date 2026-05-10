#!/bin/bash
# Safe script to remove old Linux kernels
# Keeps current kernel (6.14.0-37) and previous (6.14.0-36) as backup

set -e

CURRENT_KERNEL=$(uname -r | sed 's/-generic//')
KEEP_KERNELS="6.14.0-37 6.14.0-36"

echo "=== Old Linux Kernel Removal Script ==="
echo ""
echo "Current running kernel: ${CURRENT_KERNEL}-generic"
echo "Kernels to keep: ${KEEP_KERNELS}"
echo ""

# Find orphaned modules-extra packages (kernels removed but modules remain)
echo "Step 1: Finding orphaned kernel modules-extra packages..."
ORPHANED_MODULES=$(dpkg-query -Wf '${Package}\n' | grep "linux-modules-extra" | grep -v "6.14.0-37" | grep -v "6.14.0-36")

if [ -z "$ORPHANED_MODULES" ]; then
    echo "  ✓ No orphaned modules-extra packages found"
else
    echo "  Found orphaned packages:"
    TOTAL_SIZE=0
    echo "$ORPHANED_MODULES" | while read pkg; do
        size=$(dpkg-query -Wf '${Installed-Size}\t${Package}\n' "$pkg" 2>/dev/null | awk '{printf "%.1f", $1/1024}')
        echo "    - $pkg (${size} MB)"
    done
    
    TOTAL_SIZE=$(echo "$ORPHANED_MODULES" | while read pkg; do dpkg-query -Wf '${Installed-Size}\t${Package}\n' "$pkg" 2>/dev/null | awk '{print $1}'; done | awk '{sum+=$1} END {printf "%.1f", sum/1024}')
    echo ""
    echo "  Total size: ${TOTAL_SIZE} MB"
    echo ""
    echo "  Removing orphaned modules-extra packages..."
    echo "$ORPHANED_MODULES" | xargs sudo apt-get remove --purge -y
    echo "  ✓ Orphaned modules removed"
fi

echo ""

# Optional: Remove previous kernel (6.14.0-36) if user wants
# Uncomment the section below if you want to remove 6.14.0-36 as well
# echo "Step 2: Checking if previous kernel (6.14.0-36) should be removed..."
# echo "  Keeping 6.14.0-36 as backup (recommended for safety)"
# echo "  To remove it, uncomment the removal section in the script"

# Clean up any remaining dependencies
echo "Step 2: Cleaning up unused dependencies..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo ""
echo "=== Cleanup Complete ==="
echo ""
echo "Remaining kernels:"
dpkg -l | grep -E "^ii.*linux-image" | awk '{print "  - " $2}'
echo ""
echo "Boot directory size:"
du -sh /boot 2>/dev/null | awk '{print "  /boot: " $1}'

