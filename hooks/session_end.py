#!/usr/bin/env python3
"""
RevvTen SessionEnd hook for Claude Code.

Automatically deactivates RevvTen when a Claude Code session ends,
ensuring no stale session files remain in /tmp/revvten-sessions/.
"""

import json
import os
import sys

SESSION_DIR = '/tmp/revvten-sessions'


def main():
    try:
        data = json.load(sys.stdin)
        session_id = data.get('session_id', '')

        if session_id:
            path = os.path.join(SESSION_DIR, session_id)
            if os.path.exists(path):
                os.remove(path)

    except Exception:
        pass

    print(json.dumps({}))
    sys.exit(0)


if __name__ == '__main__':
    main()
