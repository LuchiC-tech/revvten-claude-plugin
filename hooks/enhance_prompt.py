#!/usr/bin/env python3
"""
RevvTen Prompt Enhancement Hook for Claude Code.

Hooks into UserPromptSubmit to:
  1. Handle "revvten on|off|status" commands (session activation)
  2. If session is active, enhance the user's prompt via RevvTen Desktop API
  3. Surface errors (auth, usage limits) instead of failing silently
"""

import json
import os
import sys
import urllib.request
import urllib.error

REVVTEN_API_URL = os.environ.get('REVVTEN_API_URL', 'http://localhost:3847/api/enhance')
REVVTEN_MIN_LENGTH = int(os.environ.get('REVVTEN_MIN_LENGTH', '4'))
SESSION_DIR = '/tmp/revvten-sessions'


# ---------------------------------------------------------------------------
# Session management (per Claude Code session_id)
# ---------------------------------------------------------------------------

def _session_file(session_id):
    return os.path.join(SESSION_DIR, session_id)


def is_session_active(session_id):
    return os.path.exists(_session_file(session_id))


def activate_session(session_id):
    os.makedirs(SESSION_DIR, exist_ok=True)
    with open(_session_file(session_id), 'w') as f:
        f.write('active')


def deactivate_session(session_id):
    path = _session_file(session_id)
    if os.path.exists(path):
        os.remove(path)


# ---------------------------------------------------------------------------
# "revvten" command handler
# ---------------------------------------------------------------------------

def handle_command(prompt, session_id):
    """Parse 'revvten <arg>' and return a JSON-serialisable dict."""
    arg = prompt[len('revvten'):].strip().lower()

    if arg == 'on':
        activate_session(session_id)
        return {
            "decision": "block",
            "reason": "RevvTen activated! Your prompts will now be enhanced.\n\nTo deactivate: revvten off"
        }

    if arg == 'off':
        deactivate_session(session_id)
        return {
            "decision": "block",
            "reason": "RevvTen deactivated. Prompts will pass through unchanged.\n\nTo reactivate: revvten on"
        }

    if arg == 'status':
        active = is_session_active(session_id)
        label = "active" if active else "dormant"
        return {
            "decision": "block",
            "reason": (
                f"RevvTen is {label}\n\n"
                "Commands:\n"
                "  revvten on     - activate for this session\n"
                "  revvten off    - deactivate\n"
                "  revvten status - show current state"
            )
        }

    # Unknown arg — show help
    return {
        "decision": "block",
        "reason": (
            "RevvTen - AI Prompt Enhancement\n\n"
            "Commands:\n"
            "  revvten on     - activate for this session\n"
            "  revvten off    - deactivate\n"
            "  revvten status - show current state"
        )
    }


# ---------------------------------------------------------------------------
# Prompt filter
# ---------------------------------------------------------------------------

def should_enhance(prompt):
    stripped = prompt.strip()
    if len(stripped) < REVVTEN_MIN_LENGTH:
        return False
    return True


# ---------------------------------------------------------------------------
# RevvTen Desktop API call
# ---------------------------------------------------------------------------

def call_api(prompt):
    try:
        payload = json.dumps({
            'prompt': prompt,
            'source': 'claude-code',
        }).encode('utf-8')

        req = urllib.request.Request(
            REVVTEN_API_URL,
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))

    except urllib.error.URLError:
        return {'error': 'Could not reach RevvTen Desktop. Is it running?'}
    except Exception as exc:
        return {'error': str(exc)}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get('prompt', '').strip()
        session_id = data.get('session_id', 'unknown')

        # 1. "revvten" commands — always handled, even when dormant
        if prompt.lower().startswith('revvten'):
            print(json.dumps(handle_command(prompt, session_id)))
            sys.exit(0)

        # 2. Session must be active
        if not is_session_active(session_id):
            print(json.dumps({}))
            sys.exit(0)

        # 3. Prompt must pass basic filters
        if not should_enhance(prompt):
            print(json.dumps({}))
            sys.exit(0)

        # 4. Call RevvTen Desktop
        result = call_api(prompt)

        # 4a. Surface errors to the user
        if result.get('error'):
            error_msg = result['error'] if isinstance(result['error'], str) else 'Enhancement failed'
            print(json.dumps({
                "systemMessage": f"RevvTen: {error_msg}"
            }))
            sys.exit(0)

        # 4b. No enhanced text returned
        enhanced = result.get('enhanced', '')
        if not enhanced or enhanced.strip() == prompt:
            print(json.dumps({}))
            sys.exit(0)

        # 5. Inject the enhanced prompt as additional context
        preview = (enhanced[:150] + '...') if len(enhanced) > 150 else enhanced
        print(json.dumps({
            "systemMessage": f"RevvTen enhanced your prompt. Preview: {preview}",
            "additionalContext": (
                f"<enhanced_prompt>\n{enhanced}\n</enhanced_prompt>\n\n"
                "Claude: respond to the <enhanced_prompt> above instead of the "
                "original user message."
            )
        }))

    except Exception:
        print(json.dumps({}))

    sys.exit(0)


if __name__ == '__main__':
    main()
