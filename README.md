# RevvTen - AI-Powered Prompt Enhancement for Claude Code

Automatically improve your prompts using advanced prompt engineering frameworks
for better AI responses. RevvTen is **dormant by default** and activates only
when you ask it to, giving you full control.

## Prerequisites

**[RevvTen Desktop](https://revvten.com) must be installed and running** for
this plugin to work. The plugin communicates with RevvTen Desktop's local API
on `localhost:3847`.

## Installation

```bash
git clone https://github.com/LuchiC-tech/revvten-claude-plugin.git ~/revvten-claude-plugin
cd ~/revvten-claude-plugin
./install.sh
```

Then start (or restart) Claude Code:

```bash
claude
```

The install script writes hooks to `~/.claude/settings.json` (global user scope)
so the plugin works in **every project directory**.

## Usage

RevvTen is dormant by default. Activate it each session with:

```
revvten on
```

Once active, every prompt you type is automatically enhanced before Claude sees
it.

### Commands

| Command            | Description                         |
|--------------------|-------------------------------------|
| `revvten on`       | Activate enhancement for this session |
| `revvten off`      | Deactivate enhancement              |
| `revvten status`   | Check whether RevvTen is active     |

### Example

**You type:**

```
fix the bug in auth
```

**RevvTen enhances it to:**

```
Identify and fix the authentication bug. Analyze the auth flow for
logical errors, missing validation, or incorrect token handling.
Provide the corrected code with an explanation of what was wrong.
```

Claude then responds to the enhanced version.

## How It Works

1. You start Claude Code and type `revvten on`
2. You type a prompt and press Enter
3. The `UserPromptSubmit` hook sends it to RevvTen Desktop (`localhost:3847`)
4. RevvTen Desktop enhances it using AI-powered prompt engineering frameworks
5. The enhanced prompt is injected as additional context for Claude
6. When the session ends, the `SessionEnd` hook auto-deactivates RevvTen

## Configuration

| Environment variable    | Default | Description                          |
|-------------------------|---------|--------------------------------------|
| `REVVTEN_API_URL`       | `http://localhost:3847/api/enhance` | Desktop API endpoint |
| `REVVTEN_MIN_LENGTH`    | `4`     | Minimum prompt length to enhance     |

## Requirements

- Claude Code CLI (v2.1+)
- RevvTen Desktop (running and logged in)
- Python 3.7+

## Uninstall

Remove RevvTen hooks from your global settings:

```bash
python3 -c "
import json, os, sys
p = os.path.expanduser('~/.claude/settings.json')
try:
    s = json.load(open(p))
    for event in ['UserPromptSubmit', 'SessionEnd']:
        s.get('hooks', {}).get(event, [])[:] = [
            g for g in s.get('hooks', {}).get(event, [])
            if not any('revvten' in json.dumps(h).lower() for h in g.get('hooks', []))
        ]
    json.dump(s, open(p, 'w'), indent=2)
    print('RevvTen hooks removed.')
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
"
```

Or manually edit `~/.claude/settings.json` and remove the RevvTen hook entries.

## Troubleshooting

**Hook not working in a project?**
Run `./install.sh` again. It writes to `~/.claude/settings.json` (global scope).
An older install may have written to `settings.local.json` (project scope only).

**RevvTen Desktop not responding?**
```bash
curl http://localhost:3847/health
```
If this fails, open RevvTen Desktop and make sure you are logged in.

**"Not logged in" or "Usage limit reached" errors?**
Open RevvTen Desktop, log in, or upgrade your plan.

## Manual Installation

If you prefer not to use the install script, copy the structure from
[examples/settings.json](examples/settings.json) into `~/.claude/settings.json`
and replace `/PATH/TO/` with the actual path to this repository.

## Support

- Website: https://revvten.com
- Email: support@revvten.com

## License

MIT License
