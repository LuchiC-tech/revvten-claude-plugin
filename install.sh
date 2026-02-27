#!/bin/bash
# RevvTen Claude Code Plugin Installer
#
# Safely merges RevvTen hooks into ~/.claude/settings.json (global user scope)
# so the plugin works in ALL project directories.
#
# - Backs up existing settings before modifying
# - Appends hooks (never overwrites other plugins' hooks)
# - Idempotent: safe to run multiple times

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo ""
echo "  RevvTen Claude Code Plugin Installer"
echo "  ====================================="
echo ""

# ── 1. Ensure ~/.claude/ exists ──────────────────────────────────────────────

mkdir -p "$HOME/.claude"

# ── 2. Back up existing settings ─────────────────────────────────────────────

if [ -f "$SETTINGS_FILE" ]; then
    BACKUP="$SETTINGS_FILE.backup.$(date +%s)"
    cp "$SETTINGS_FILE" "$BACKUP"
    echo "  Backed up existing settings to:"
    echo "    $BACKUP"
    echo ""
fi

# ── 3. Merge hooks into settings.json using Python ──────────────────────────

python3 - "$SETTINGS_FILE" "$PLUGIN_DIR" << 'PYEOF'
import json
import sys
import os

settings_path = sys.argv[1]
plugin_dir    = sys.argv[2]

enhance_cmd  = f"python3 {plugin_dir}/hooks/enhance_prompt.py"
session_cmd  = f"python3 {plugin_dir}/hooks/session_end.py"

# Load existing settings (or start fresh)
try:
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    if not isinstance(settings, dict):
        settings = {}
except (FileNotFoundError, json.JSONDecodeError):
    settings = {}

hooks = settings.setdefault('hooks', {})

# --- UserPromptSubmit ---------------------------------------------------------

def _has_revvten(hook_list, marker='enhance_prompt.py'):
    """Check whether a RevvTen hook is already registered."""
    for group in hook_list:
        for h in group.get('hooks', []):
            if marker in h.get('command', ''):
                return True
    return False

ups = hooks.setdefault('UserPromptSubmit', [])

if _has_revvten(ups, 'enhance_prompt.py'):
    # Update the existing entry in-place (path may have changed)
    for group in ups:
        for h in group.get('hooks', []):
            if 'enhance_prompt.py' in h.get('command', ''):
                h['command'] = enhance_cmd
                h['timeout'] = 15
else:
    ups.append({
        "hooks": [
            {
                "type": "command",
                "command": enhance_cmd,
                "timeout": 15,
            }
        ]
    })

# --- SessionEnd ---------------------------------------------------------------

se = hooks.setdefault('SessionEnd', [])

if _has_revvten(se, 'session_end.py'):
    for group in se:
        for h in group.get('hooks', []):
            if 'session_end.py' in h.get('command', ''):
                h['command'] = session_cmd
else:
    se.append({
        "hooks": [
            {
                "type": "command",
                "command": session_cmd,
            }
        ]
    })

# --- Write back ---------------------------------------------------------------

with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2)
    f.write('\n')

PYEOF

echo "  Hooks installed to:"
echo "    $SETTINGS_FILE"
echo ""

# ── 4. Clean up old settings.local.json entry (if present) ──────────────────

OLD_LOCAL="$HOME/.claude/settings.local.json"
if [ -f "$OLD_LOCAL" ] && grep -q 'enhance_prompt.py' "$OLD_LOCAL" 2>/dev/null; then
    echo "  Found old RevvTen config in settings.local.json"
    echo "  (This file is project-scoped and was the cause of the"
    echo "   'works from home but not inside projects' bug.)"
    echo ""
    echo "  Removing RevvTen entries from settings.local.json..."
    # If it only contains RevvTen hooks, just delete it
    CONTENT=$(cat "$OLD_LOCAL")
    if echo "$CONTENT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
hooks = d.get('hooks', {})
only_revvten = all('enhance_prompt.py' in json.dumps(v) or 'revvten' in json.dumps(v).lower() for v in hooks.values())
sys.exit(0 if only_revvten else 1)
" 2>/dev/null; then
        rm "$OLD_LOCAL"
        echo "  Deleted settings.local.json (contained only RevvTen hooks)"
    else
        echo "  settings.local.json contains other hooks; left it in place."
        echo "  You may want to manually remove the RevvTen entries."
    fi
    echo ""
fi

# ── 5. Done ──────────────────────────────────────────────────────────────────

echo "  ================================================"
echo "  Installation complete!"
echo "  ================================================"
echo ""
echo "  How to use:"
echo ""
echo "    1. Make sure RevvTen Desktop is running"
echo "       (download from https://revvten.com)"
echo ""
echo "    2. Start (or restart) Claude Code:"
echo "       $ claude"
echo ""
echo "    3. Activate RevvTen for the session:"
echo "       revvten on"
echo ""
echo "    4. Type any prompt — it will be enhanced!"
echo ""
echo "  Commands:"
echo "    revvten on     — activate for this session"
echo "    revvten off    — deactivate"
echo "    revvten status — check current state"
echo ""
