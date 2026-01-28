#!/bin/bash
# RevvTen Claude Code Plugin Installer
# Automatically configures Claude Code hooks for prompt enhancement

set -e

# Get the directory where this script is located
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 Installing RevvTen Claude Code Plugin..."
echo ""

# Create Claude config directory if it doesn't exist
mkdir -p ~/.claude

# Check if settings.local.json already exists
if [ -f ~/.claude/settings.local.json ]; then
    echo "⚠️  Found existing ~/.claude/settings.local.json"
    echo "   Backing up to ~/.claude/settings.local.json.backup"
    cp ~/.claude/settings.local.json ~/.claude/settings.local.json.backup
fi

# Write settings.local.json with the correct path
cat > ~/.claude/settings.local.json << HOOKEOF
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${PLUGIN_DIR}/hooks/enhance_prompt.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
HOOKEOF

echo "✅ Hook installed to ~/.claude/settings.local.json"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Next steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  1. Make sure RevvTen Desktop is running"
echo "     (Download from https://revvten.com if needed)"
echo ""
echo "  2. Restart Claude Code:"
echo "     $ claude"
echo ""
echo "  3. Type any prompt - RevvTen will enhance it!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Installation complete! 🎉"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
