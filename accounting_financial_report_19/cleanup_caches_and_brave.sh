#!/bin/bash
# Script to clean JetBrains cache, browser caches, and remove Brave browser
# Docker is left untouched

set -e

echo "=== Cache Cleanup and Brave Removal Script ==="
echo ""

TOTAL_FREED=0

# 1. Clean JetBrains cache
echo "1. Cleaning JetBrains cache..."
if [ -d "$HOME/.cache/JetBrains" ]; then
    JETBRAINS_SIZE=$(du -sb "$HOME/.cache/JetBrains" 2>/dev/null | awk '{print $1}')
    JETBRAINS_SIZE_MB=$(echo "scale=2; $JETBRAINS_SIZE/1024/1024" | bc)
    echo "   Current size: ${JETBRAINS_SIZE_MB} MB"
    rm -rf "$HOME/.cache/JetBrains"/*
    echo "   ✓ JetBrains cache cleared (${JETBRAINS_SIZE_MB} MB freed)"
    TOTAL_FREED=$((TOTAL_FREED + JETBRAINS_SIZE))
else
    echo "   No JetBrains cache found"
fi
echo ""

# 2. Clean Chrome cache
echo "2. Cleaning Google Chrome cache..."
if [ -d "$HOME/.cache/google-chrome" ]; then
    CHROME_SIZE=$(du -sb "$HOME/.cache/google-chrome" 2>/dev/null | awk '{print $1}')
    CHROME_SIZE_MB=$(echo "scale=2; $CHROME_SIZE/1024/1024" | bc)
    echo "   Current size: ${CHROME_SIZE_MB} MB"
    rm -rf "$HOME/.cache/google-chrome"/*
    echo "   ✓ Chrome cache cleared (${CHROME_SIZE_MB} MB freed)"
    TOTAL_FREED=$((TOTAL_FREED + CHROME_SIZE))
else
    echo "   No Chrome cache found"
fi
echo ""

# 3. Clean Brave cache (before removal)
echo "3. Cleaning Brave browser cache..."
if [ -d "$HOME/.cache/BraveSoftware" ]; then
    BRAVE_CACHE_SIZE=$(du -sb "$HOME/.cache/BraveSoftware" 2>/dev/null | awk '{print $1}')
    BRAVE_CACHE_SIZE_MB=$(echo "scale=2; $BRAVE_CACHE_SIZE/1024/1024" | bc)
    echo "   Current size: ${BRAVE_CACHE_SIZE_MB} MB"
    rm -rf "$HOME/.cache/BraveSoftware"/*
    echo "   ✓ Brave cache cleared (${BRAVE_CACHE_SIZE_MB} MB freed)"
    TOTAL_FREED=$((TOTAL_FREED + BRAVE_CACHE_SIZE))
else
    echo "   No Brave cache found"
fi
echo ""

# 4. Remove Brave browser
echo "4. Removing Brave browser..."
BRAVE_PACKAGES=$(dpkg -l | grep -i brave | awk '{print $2}')

if [ -z "$BRAVE_PACKAGES" ]; then
    echo "   No Brave packages found"
else
    echo "   Found Brave packages:"
    echo "$BRAVE_PACKAGES" | while read pkg; do
        size=$(dpkg-query -Wf '${Installed-Size}\t${Package}\n' "$pkg" 2>/dev/null | awk '{printf "%.1f", $1/1024}')
        echo "     - $pkg (${size} MB)"
    done
    
    BRAVE_SIZE=$(dpkg-query -Wf '${Installed-Size}\t${Package}\n' | grep -i brave | awk '{sum+=$1} END {print sum}')
    BRAVE_SIZE_MB=$(echo "scale=2; $BRAVE_SIZE/1024" | bc)
    
    echo ""
    echo "   Removing Brave browser..."
    echo "$BRAVE_PACKAGES" | xargs sudo apt-get remove --purge -y
    
    # Also remove Brave data directories
    if [ -d "$HOME/.config/BraveSoftware" ]; then
        rm -rf "$HOME/.config/BraveSoftware"
        echo "   ✓ Removed Brave configuration"
    fi
    if [ -d "$HOME/.local/share/BraveSoftware" ]; then
        rm -rf "$HOME/.local/share/BraveSoftware"
        echo "   ✓ Removed Brave user data"
    fi
    if [ -d "/opt/brave.com" ]; then
        sudo rm -rf /opt/brave.com
        echo "   ✓ Removed Brave installation directory"
    fi
    
    echo "   ✓ Brave browser removed (${BRAVE_SIZE_MB} MB freed)"
    TOTAL_FREED=$((TOTAL_FREED + BRAVE_SIZE * 1024))
fi
echo ""

# Clean up any unused dependencies
echo "5. Cleaning up unused dependencies..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo ""
echo "=== Cleanup Complete ==="
TOTAL_FREED_MB=$(echo "scale=2; $TOTAL_FREED/1024/1024" | bc)
echo "Total space freed: ${TOTAL_FREED_MB} MB (~$(echo "scale=2; $TOTAL_FREED_MB/1024" | bc) GB)"
echo ""
echo "Note: Docker was left untouched as requested."

