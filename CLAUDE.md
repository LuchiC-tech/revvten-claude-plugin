# CLAUDE.md — RevvTen Claude Code Plugin

## Company Context
You are working on RevvTen — the invisible intelligence layer between humans and every AI tool they use. Before making any changes, understand the full context:
- Vision & Mission: See revten-context/VISION.md
- Product Map: See revten-context/PRODUCT.md
- System Architecture: See revten-context/ARCHITECTURE.md
- Safety Rules: See revten-context/SAFETY-RULES.md (FOLLOW EVERY RULE)
- Current Priorities: See revten-context/CURRENT-PRIORITIES.md

## This Repo
The Claude Code Plugin intercepts every prompt the user types in Claude Code via a UserPromptSubmit hook. When enabled (via `revvten on`), it POSTs the raw prompt to the locally-running RevvTen Desktop app (localhost:3847) and injects the AI-enhanced version as additionalContext so Claude responds to the improved prompt.

This is NOT a cloud API integration — it talks exclusively to a local HTTP server that the RevvTen Desktop app exposes. No Supabase, no enterprise auth, no MCP servers, no skills. Pure hook-based plugin.

### User Commands (typed as prompts)
- `revvten on` — activates enhancement for current session
- `revvten off` — deactivates it
- `revvten status` — shows whether it's active

## Tech Stack
- Language: Python 3 (hooks), Bash (installer)
- Plugin format: Claude Code hook-based plugin (no MCP, no npm package)
- Dependencies: Python stdlib only (json, urllib.request, os, sys)
- External runtime: RevvTen Desktop app must be running on port 3847
- Package manager: None

## Plugin Structure
```
revvten-claude-plugin/
├── .claude-plugin/
│   └── plugin.json              # Manifest: name=revvten, version=1.0.0, category=productivity
├── hooks/
│   ├── hooks.json               # UserPromptSubmit + SessionEnd hook definitions
│   ├── enhance_prompt.py        # Main hook: enhancement + revvten on/off/status
│   └── session_end.py           # Cleanup: deletes session state file
├── examples/
│   └── settings.json            # Template for ~/.claude/settings.json
├── install.sh                   # One-command installer: patches ~/.claude/settings.json
├── README.md
└── .gitignore
```

### Hook Registration (hooks/hooks.json)
- UserPromptSubmit → python3 ${CLAUDE_PLUGIN_ROOT}/hooks/enhance_prompt.py
- SessionEnd → python3 ${CLAUDE_PLUGIN_ROOT}/hooks/session_end.py

### Session State
Stored as empty marker files at /tmp/revvten-sessions/<session_id>. File exists = active. Deleted on `revvten off` or session end.

## Development Commands
```bash
# Install (patches ~/.claude/settings.json):
chmod +x install.sh && ./install.sh

# Test the hook manually:
echo '{"session_id":"test123","prompt":"write a function"}' | python3 hooks/enhance_prompt.py

# Test session end:
echo '{"session_id":"test123"}' | python3 hooks/session_end.py

# Override API endpoint:
REVVTEN_API_URL=http://localhost:9999/api/enhance python3 hooks/enhance_prompt.py
```

Requirements: Python 3 (any recent version), RevvTen Desktop running on port 3847.

## Integration Details
- Endpoint: POST http://localhost:3847/api/enhance
- Payload: {"prompt": "<raw text>", "source": "claude-code"}
- Response: response["enhanced_prompt"]
- Timeout: 90 seconds
- On failure: passes original prompt through with warning systemMessage
- Configurable via env: REVVTEN_API_URL, REVVTEN_MIN_LENGTH (default: 4 chars)

## Branch Strategy
- `main` — release — NEVER push directly
- `dev` — integration branch (agents push here)
- `feature/*` — feature branches
- `fix/*` — bug fix branches

## What NOT to Touch Without Human Review
- .claude-plugin/plugin.json — plugin manifest/identity
- install.sh — user settings.json patching logic
- hooks/hooks.json — hook registration spec
- localhost:3847 URL in enhance_prompt.py — sole integration point with Desktop app
- additionalContext/systemMessage keys in enhance_prompt.py — Claude Code hook protocol fields
- /tmp/revvten-sessions/ path — changing orphans active sessions

**Safe to modify**: REVVTEN_MIN_LENGTH default, error message strings, session_end.py cleanup logic, README.
