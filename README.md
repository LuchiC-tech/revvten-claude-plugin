# RevvTen - AI-Powered Prompt Enhancement for Claude Code

Automatically improve your prompts using advanced prompt engineering frameworks for better AI responses.

## Prerequisites

**You must have [RevvTen Desktop](https://revvten.com) installed and running** for this plugin to work.

## Installation

### Step 1: Clone this repo
```bash
git clone https://github.com/LuchiC-tech/revvten-claude-plugin.git ~/revvten-claude-plugin
```

### Step 2: Configure Claude Code hooks

Create the file `~/.claude/settings.local.json` with this content:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/revvten-claude-plugin/hooks/enhance_prompt.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

Or run this command:
```bash
mkdir -p ~/.claude && cat > ~/.claude/settings.local.json << 'HOOKEOF'
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/revvten-claude-plugin/hooks/enhance_prompt.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
HOOKEOF
```

### Step 3: Restart Claude Code
```bash
claude
```

## Usage

Once installed, RevvTen automatically enhances your prompts when you type in Claude Code.

### Example

**You type:**
```
write a function to sort an array
```

**RevvTen shows:**
```
âœRevvTen Enhanced Your Prompt

Preview: As a senior software engineer specializing in algorithm design, create a comprehensive sorting function...

<enhanced_prompt>
As a senior software engineer specializing in algorithm design, create a 
comprehensive sorting function with the following specifications:
- Multiple sorting strategies (QuickSort, MergeSort)
- Time and space complexity analysis
- Clean, well-commented implementation
- Unit tests covering edge cases
</enhanced_prompt>
```

Claude then responds to the enhanced prompt!

## How It Works

1. You type a prompt in Claude Code and press Enter
2. The hook intercepts it and sends to RevvTen Desktop (localhost:3847)
3. RevvTen enhances it using AI-powered prompt engineering frameworks
4. You see the enhanced prompt preview
5. Claude responds to the enhanced version

## Configuration

Set environment variables to customize:
```bash
export REVVTEN_ENABLED=true        # Enable/disable (default: true)
export REVVTEN_MIN_LENGTH=20       # Min prompt length to enhance (default: 20)
```

## Requirements

- Claude Code CLI (v2.1+)
- RevvTen Desktop (running and logged in)
- Python 3.7+

## Troubleshooting

**Hook not working?**
1. Make sure RevvTen Desktop is running: `curl http://localhost:3847/health`
2. Make sure you're logged in to RevvTen Desktop
3. Check the hook file exists: `ls ~/revvten-claude-plugin/hooks/enhance_prompt.py`
4. Restart Claude Code after adding the hook config

**"Session expired" error?**
- Open RevvTen Desktop and log in again

## Support

- Website: https://revvten.com
- Email: support@revvten.com

## License

MIT License
