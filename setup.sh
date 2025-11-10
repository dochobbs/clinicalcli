#!/bin/bash
# Setup script for Clinical CLI

set -e

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

# Check for API key
echo ""
echo "Checking for ANTHROPIC_API_KEY..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not found in environment"
    echo ""
    echo "Please ensure your API key is set in ~/.zshrc:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Then restart your terminal or run: source ~/.zshrc"
else
    echo "✓ ANTHROPIC_API_KEY found"
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
echo "  alias clinical='cd /Users/dochobbs/Downloads/Consult/Claude/clinical-cli && source .venv/bin/activate && python src/cli.py'"
echo ""
echo "Then use: clinical cds, clinical note, etc."
echo ""
echo "Run 'python src/cli.py --help' to see available commands"
