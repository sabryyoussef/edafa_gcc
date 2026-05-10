#!/bin/bash
# Script to remove disabled snap package revisions
# Only removes disabled versions, keeps active versions intact

set -e

echo "=== Disabled Snap Package Removal Script ==="
echo ""

# Find disabled snap revisions
DISABLED_SNAPS=$(snap list --all 2>/dev/null | grep disabled | awk '{print $1, $3}')

if [ -z "$DISABLED_SNAPS" ]; then
    echo "✓ No disabled snap packages found"
    exit 0
fi

echo "Found disabled snap revisions:"
echo "$DISABLED_SNAPS" | while read name revision; do
    active_version=$(snap list --all 2>/dev/null | grep "^$name" | grep -v disabled | head -1 | awk '{print $2, "(" $3 ")"}')
    size=$(du -sh /var/lib/snapd/snaps/${name}_${revision}.snap 2>/dev/null | awk '{print $1}')
    echo "  - $name (revision $revision) - $size"
    echo "    Active version: $active_version (will be kept)"
done

echo ""
echo "Removing disabled snap revisions..."
echo ""

TOTAL_FREED=0
echo "$DISABLED_SNAPS" | while read name revision; do
    echo "Removing $name (revision $revision)..."
    if sudo snap remove "$name" --revision="$revision" 2>&1; then
        size=$(du -sb /var/lib/snapd/snaps/${name}_${revision}.snap 2>/dev/null | awk '{print $1}' || echo "0")
        echo "  ✓ Removed successfully"
    else
        echo "  ✗ Failed to remove (may already be removed)"
    fi
done

echo ""
echo "=== Cleanup Complete ==="
echo ""
echo "Remaining snap packages:"
snap list 2>/dev/null | tail -n +2 | awk '{print "  ✓ " $1 " (" $2 ")"}'

echo ""
echo "Note: Active versions of all packages have been preserved."

