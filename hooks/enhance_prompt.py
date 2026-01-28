#!/usr/bin/env python3
"""
RevvTen Prompt Enhancement Hook for Claude Code

This hook intercepts user prompts and enhances them using RevvTen's
AI-powered prompt engineering frameworks.
"""

import json
import sys
import os
import urllib.request
import urllib.error

# RevvTen API configuration
REVVTEN_API_URL = os.environ.get('REVVTEN_API_URL', 'http://localhost:3847/api/enhance')
REVVTEN_ENABLED = os.environ.get('REVVTEN_ENABLED', 'true').lower() == 'true'
REVVTEN_AUTO_ENHANCE = os.environ.get('REVVTEN_AUTO_ENHANCE', 'false').lower() == 'true'
REVVTEN_MIN_LENGTH = int(os.environ.get('REVVTEN_MIN_LENGTH', '20'))

def should_enhance(prompt: str) -> bool:
    """Determine if a prompt should be enhanced."""
    if len(prompt.strip()) < REVVTEN_MIN_LENGTH:
        return False
    if prompt.strip().startswith('/'):
        return False
    simple_responses = {'yes', 'no', 'y', 'n', 'ok', 'okay', 'sure', 'thanks', 'thank you', 'done', 'continue', 'go ahead'}
    if prompt.strip().lower() in simple_responses:
        return False
    return True

def call_revvten_api(prompt: str) -> dict:
    """Call RevvTen API to enhance the prompt."""
    try:
        data = json.dumps({
            'prompt': prompt,
            'source': 'claude-code-plugin',
            'options': {
                'autoSelect': True,
                'includeFramework': True
            }
        }).encode('utf-8')
        
        req = urllib.request.Request(
            REVVTEN_API_URL,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'RevvTen-ClaudeCode-Plugin/1.0'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    
    except urllib.error.URLError as e:
        return {'error': f'Network error: {str(e)}', 'enhanced': None}
    except json.JSONDecodeError as e:
        return {'error': f'Invalid response: {str(e)}', 'enhanced': None}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}', 'enhanced': None}

def format_enhancement_message(original: str, enhanced: str, framework: str = None) -> str:
    """Format the enhancement suggestion message."""
    msg_parts = ["✨ **RevvTen Prompt Enhancement Available**\n"]
    if framework:
        msg_parts.append(f"Framework: {framework}\n")
    msg_parts.append("\n**Enhanced prompt:**\n")
    msg_parts.append(f"```\n{enhanced}\n```\n")
    msg_parts.append("\n*Tip: Set REVVTEN_AUTO_ENHANCE=true to auto-apply enhancements*")
    return ''.join(msg_parts)

def main():
    """Main entry point for the UserPromptSubmit hook."""
    try:
        input_data = json.load(sys.stdin)
        user_prompt = input_data.get('user_prompt', '')
        
        if not REVVTEN_ENABLED:
            print(json.dumps({}))
            sys.exit(0)
        
        if not should_enhance(user_prompt):
            print(json.dumps({}))
            sys.exit(0)
        
        result = call_revvten_api(user_prompt)
        
        if 'error' in result onot result.get('enhanced'):
            print(json.dumps({}))
            sys.exit(0)
        
        enhanced_prompt = result.get('enhanced', '')
        framework = result.get('framework', '')
        
        if not enhanced_prompt or enhanced_prompt.strip() == user_prompt.strip():
            print(json.dumps({}))
            sys.exit(0)
        
        response = {}
        
        if REVVTEN_AUTO_ENHANCE:
            response['hookSpecificOutput'] = {
                'updatedInput': {
                    'user_prompt': enhanced_prompt
                }
            }
            response['systemMessage'] = f"✨ RevvTen auto-enhanced your prompt using {framework} framework."
        else:
            response['systemMessage'] = format_enhancement_message(
                user_prompt, 
                enhanced_prompt, 
                framework
            )
        
        print(json.dumps(response))
    
    except Exception as e:
        error_output = {}
        if os.environ.get('REVVTEN_DEBUG'
            error_output = {"systemMessage": f"RevvTen: {str(e)}"}
        print(json.dumps(error_output))
    
    finally:
        sys.exit(0)

if __name__ == '__main__':
    main()
