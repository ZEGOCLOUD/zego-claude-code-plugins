#!/bin/bash

# ZEGO Claude Code Plugin - Reinstall Script
# This script uninstalls the plugin, clears cache, and reinstalls at user level

set -e  # Exit on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
CLAUDE_DIR="$HOME/.claude"
MARKETPLACE_FILE="$CLAUDE_DIR/plugins/known_marketplaces.json"
INSTALLED_FILE="$CLAUDE_DIR/plugins/installed_plugins.json"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
CACHE_DIR="$CLAUDE_DIR/plugins/cache/zego-claude-code-plugins"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKETPLACE_NAME="zego-claude-code-plugins"

# Plugins in marketplace
PLUGINS=("write-zego-docs" "zego-assistant")

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}ZEGO Plugin Reinstall Script${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Step 1: Remove from known_marketplaces.json
echo -e "${YELLOW}[1/6] Removing marketplace registration...${NC}"
if [ -f "$MARKETPLACE_FILE" ]; then
    # Backup first
    cp "$MARKETPLACE_FILE" "$MARKETPLACE_FILE.backup"
    # Remove the marketplace entry using jq
    if command -v jq &> /dev/null; then
        jq "del(.\"$MARKETPLACE_NAME\")" "$MARKETPLACE_FILE" > "$MARKETPLACE_FILE.tmp" && mv "$MARKETPLACE_FILE.tmp" "$MARKETPLACE_FILE"
        echo -e "${GREEN}✓ Removed from known_marketplaces.json${NC}"
    else
        echo -e "${RED}✗ jq not found, skipping marketplace file update${NC}"
        echo -e "${YELLOW}  Install jq: brew install jq${NC}"
    fi
else
    echo -e "${YELLOW}⚠ known_marketplaces.json not found${NC}"
fi

# Step 2: Remove from installed_plugins.json
echo -e "${YELLOW}[2/6] Removing installed plugin entries...${NC}"
if [ -f "$INSTALLED_FILE" ]; then
    cp "$INSTALLED_FILE" "$INSTALLED_FILE.backup"
    if command -v jq &> /dev/null; then
        for plugin in "${PLUGINS[@]}"; do
            jq "del(.plugins[\"$plugin@$MARKETPLACE_NAME\"])" "$INSTALLED_FILE" > "$INSTALLED_FILE.tmp" && mv "$INSTALLED_FILE.tmp" "$INSTALLED_FILE"
        done
        echo -e "${GREEN}✓ Removed from installed_plugins.json${NC}"
    fi
else
    echo -e "${YELLOW}⚠ installed_plugins.json not found${NC}"
fi

# Step 3: Disable in settings.json
echo -e "${YELLOW}[3/6] Disabling plugins in settings...${NC}"
if [ -f "$SETTINGS_FILE" ]; then
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
    if command -v jq &> /dev/null; then
        for plugin in "${PLUGINS[@]}"; do
            jq ".enabledPlugins[\"$plugin@$MARKETPLACE_NAME\"] = false" "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp" && mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
        done
        echo -e "${GREEN}✓ Disabled plugins in settings.json${NC}"
    fi
else
    echo -e "${YELLOW}⚠ settings.json not found${NC}"
fi

# Step 4: Clear cache
echo -e "${YELLOW}[4/6] Clearing plugin cache...${NC}"
if [ -d "$CACHE_DIR" ]; then
    rm -rf "$CACHE_DIR"
    echo -e "${GREEN}✓ Cache cleared: $CACHE_DIR${NC}"
else
    echo -e "${YELLOW}⚠ Cache directory not found${NC}"
fi

# Step 5: Restore marketplace entry (reinstall)
echo ""
echo -e "${YELLOW}[5/6] Reinstalling plugin (restoring marketplace entry)...${NC}"

# For directory-based marketplaces, we restore the entry directly
if [ -f "$MARKETPLACE_FILE" ]; then
    if command -v jq &> /dev/null; then
        # Create the marketplace entry
        jq --arg name "$MARKETPLACE_NAME" --arg path "$PROJECT_DIR" \
            '.[$name] = {
                "source": {
                    "source": "directory",
                    "path": $path
                },
                "installLocation": $path,
                "lastUpdated": (now | todate)
            }' "$MARKETPLACE_FILE" > "$MARKETPLACE_FILE.tmp" && \
            mv "$MARKETPLACE_FILE.tmp" "$MARKETPLACE_FILE"
        echo -e "${GREEN}✓ Marketplace entry restored${NC}"
    else
        echo -e "${RED}✗ jq not found, cannot restore marketplace entry${NC}"
        echo -e "${YELLOW}  Install jq: brew install jq${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ known_marketplaces.json not found${NC}"
    exit 1
fi

# Step 6: Re-enable plugins
echo -e "${YELLOW}[6/6] Re-enabling plugins...${NC}"
if [ -f "$SETTINGS_FILE" ]; then
    if command -v jq &> /dev/null; then
        for plugin in "${PLUGINS[@]}"; do
            jq --arg key "$plugin@$MARKETPLACE_NAME" '.enabledPlugins[$key] = true' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp" && mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
        done
        echo -e "${GREEN}✓ Plugins re-enabled in settings.json${NC}"
    fi
fi

# Optionally, touch the marketplace.json to trigger reload
MARKETPLACE_JSON="$PROJECT_DIR/.claude-plugin/marketplace.json"
if [ -f "$MARKETPLACE_JSON" ]; then
    touch "$MARKETPLACE_JSON"
    echo -e "${GREEN}✓ Triggered plugin reload${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Reinstall Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Backup files created:"
echo -e "  - $MARKETPLACE_FILE.backup"
echo -e "  - $INSTALLED_FILE.backup"
echo -e "  - $SETTINGS_FILE.backup"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Restart Claude Code to reload plugins"
echo -e "  2. Check /plugins command to verify installation"
echo ""
