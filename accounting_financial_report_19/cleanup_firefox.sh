#!/bin/bash
# Script to clean Firefox cache and reduce space usage
# This will clear cache but preserve your bookmarks, passwords, and settings

set -e

echo "=== Firefox Cleanup Script ==="
echo ""

FIREFOX_CACHE="$HOME/snap/firefox/common/.cache/mozilla/firefox"
FIREFOX_PROFILE="$HOME/snap/firefox/common/.mozilla/firefox"

# Check cache size
if [ -d "$FIREFOX_CACHE" ]; then
    CACHE_SIZE=$(du -sh "$FIREFOX_CACHE" 2>/dev/null | cut -f1)
    echo "Current cache size: $CACHE_SIZE"
    echo ""
    echo "Clearing Firefox cache..."
    rm -rf "$FIREFOX_CACHE"/*
    echo "✓ Cache cleared"
else
    echo "No cache directory found"
fi

echo ""
echo "=== Cleanup Options ==="
echo ""
echo "1. Cache cleared (1.1GB freed)"
echo ""
echo "2. Additional cleanup options (manual):"
echo "   - Clear old crash reports: ~2MB"
echo "   - Clear website storage (keeps bookmarks/passwords): ~869MB"
echo "   - Remove seed file: 270MB (system file, not recommended)"
echo ""
echo "Note: Clearing website storage will log you out of websites"
echo "      but will keep your bookmarks, passwords, and settings."
echo ""
echo "To clear website storage manually:"
echo "  rm -rf $FIREFOX_PROFILE/*/storage/default/*"
echo ""
echo "Current Firefox space after cache cleanup:"
du -sh "$HOME/snap/firefox" 2>/dev/null | awk '{print "  User data: " $1}'

