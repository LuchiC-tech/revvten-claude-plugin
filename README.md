# RevvTen - AI-Powered Prompt Enhancement for Claude Code

Automatically improve your prompts using advanced prompt engineering frameworks for better AI responses.

## Features

- 🚀 **Automatic Enhancement**: Intercepts your prompts and suggests improvements
- 🎯 **Smart Framework Selection**: Uses the best prompt engineering framework for each task
- ⚡ **Non-Blocking**: Suggestions are optional and won't slow you down
- 🔧 **Configurable**: Control when and how enhancements are applied

## Prerequisites

**You must have [RevvTen Desktop](https://revvten.com) running** for this plugin to work. The plugin communicates with RevvTen Desktop's local API to enhance your prompts.

## Installation

In Clau run:
```bash
/plugin install revvten@https://github.com/LuchiC-tech/revvten-claude-plugin.git
```

## Usage

Once installed, RevvTen automatically analyzes your prompts and suggests enhancements.

### Example

**Original prompt:**
```
write a function to sort an array
```

**Enhanced prompt (R-T-F Framework):**
```
Role: You are an expert software engineer specializing in algorithm design.
Task: Write a function to sort an array of integers in ascending order.
Format: Provide the implementation in Python with:
- Clear docstring explaining the algorithm
- Time and space complexity analysis
- Example usage with test cases
```

## Configuration

Set environment variables to customize behavior:
```bash
export REVVTEN_ENABLED=true           # Enable/disable (default: true)
export REVVTEN_AUTO_ENHANCE=false     # Auto-apply enhancements (default: false)
export REVVTEN_MIN_LENGTH=20          # Min prompt length to trigger (default: 20)
export REVVTEN_DEBUG=false            # Show debug messages (default: false)
```

## How It Works

1. You type a prompt in Claude Code
2. The plugin sends it to RevvTen Desktop (localhost:3847)
3. RevvTen analyzes and enhances using optimal prompt engineering frameworks
4. The enhanced prompt is shown as a suggestion (or auto-applied)

## Support

- Website: https://revvten.com
- Email: support@revvten.com

## License

MIT License
