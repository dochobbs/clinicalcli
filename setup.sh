#!/bin/bash
# Setup script for Clinical CLI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🏥 Clinical CLI Setup"
echo "===================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
}

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for cloud-provider API keys
echo ""
echo "Checking cloud model credentials..."
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  No Anthropic or OpenAI API key found"
    echo ""
    echo "Cloud models require the corresponding provider key:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    echo "Local Ollama and LM Studio models can be used without a cloud key."
else
    [ -n "$ANTHROPIC_API_KEY" ] && echo "✓ ANTHROPIC_API_KEY found"
    [ -n "$OPENAI_API_KEY" ] && echo "✓ OPENAI_API_KEY found"
fi

# Make CLI executable
echo ""
echo "Making CLI executable..."
chmod +x src/cli.py

# Create convenience alias suggestion
echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the CLI:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Run commands: python src/cli.py <command>"
echo ""
echo "Optional: Add this alias to your ~/.zshrc for easier access:"
echo "  alias clinical='$SCRIPT_DIR/clinical-shell'"
echo ""
echo "Then use: clinical cds, clinical note, etc."
echo ""
echo "Run 'python src/cli.py --help' to see available commands"
