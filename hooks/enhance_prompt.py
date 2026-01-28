#!/usr/bin/env python3
"""RevvTen Prompt Enhancement Hook for Claude Code"""

import json, sys, os, urllib.request, urllib.error

REVVTEN_API_URL = os.environ.get('REVVTEN_API_URL', 'http://localhost:3847/api/enhance')
REVVTEN_ENABLED = os.environ.get('REVVTEN_ENABLED', 'true').lower() == 'true'
REVVTEN_MIN_LENGTH = int(os.environ.get('REVVTEN_MIN_LENGTH', '20'))

def should_enhance(prompt):
    if len(prompt.strip()) < REVVTEN_MIN_LENGTH: return False
    if prompt.strip().startswith('/'): return False
    if prompt.strip().lower() in {'yes','no','y','n','ok','okay','sure','thanks','thank you','done','continue','go ahead'}: return False
    return True

def call_api(prompt, metadata=None):
    try:
        payload = {'prompt': prompt, 'source': 'claude-code-plugin', 'options': {'autoSelect': True, 'includeFramework': True}}
        if metadata: payload['metadata'] = {'session_id': metadata.get('session_id'), 'cwd': metadata.get('cwd')}
        req = urllib.request.Request(REVVTEN_API_URL, json.dumps(payload).encode('utf-8'), 
            {'Content-Type': 'application/json', 'User-Agent': 'RevvTen-ClaudeCode-Plugin/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r: return json.loads(r.read().decode('utf-8'))
    except: return {'error': True}

def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get('prompt', '')
        if not REVVTEN_ENABLED or not should_enhance(prompt):
            print(json.dumps({})); sys.exit(0)
        result = call_api(prompt, data)
        if result.get('error') or not result.get('enhanced'):
            print(json.dumps({})); sys.exit(0)
        enhanced = result['enhanced']
        if not enhanced or enhanced.strip() == prompt.strip():
            print(json.dumps({})); sys.exit(0)
        
        # Show user a preview, instruct Claude to use enhanced version
        preview = enhanced[:150] + "..." if len(enhanced) > 150 else enhanced
        msg = f"""✨ **RevvTen Enhanced Your Prompt**

**Preview:** {preview}

<enhanced_prompt>
{enhanced}
</enhanced_prompt>

Claude: Please respond to the <enhanced_prompt> above instead of the original user message."""
        
        print(json.dumps({"systemMessage": msg}))
    except: print(json.dumps({}))
    finally: sys.exit(0)

if __name__ == '__main__': main()
