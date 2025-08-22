#!/bin/bash
# RevGen Installation Script
# One-command setup for the Reverse Shell Genie

set -e

echo "🧞‍♂️ RevGen Installation Script"
echo "================================="

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "✅ Python $PYTHON_VERSION found"
    
    # Check if version is 3.6+
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 6) else 1)'; then
        echo "✅ Python version is compatible"
    else
        echo "❌ Python 3.6+ is required"
        exit 1
    fi
else
    echo "❌ Python 3 not found. Please install Python 3.6+"
    exit 1
fi

# Make scripts executable
echo "Setting up RevGen..."
chmod +x revgen.py
chmod +x demo.py

# Test the installation
echo "Testing RevGen..."
if python3 revgen.py --version &> /dev/null; then
    echo "✅ RevGen is working correctly!"
else
    echo "❌ RevGen test failed"
    exit 1
fi

# Optional: Install to PATH
read -p "Do you want to create a symlink in /usr/local/bin? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [[ $EUID -eq 0 ]]; then
        ln -sf "$(pwd)/revgen.py" /usr/local/bin/revgen
        echo "✅ RevGen installed to /usr/local/bin/revgen"
        echo "You can now run 'revgen' from anywhere!"
    else
        echo "Please run with sudo to install to system PATH:"
        echo "sudo ln -sf $(pwd)/revgen.py /usr/local/bin/revgen"
    fi
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Quick start:"
echo "  ./revgen.py --list"
echo "  ./revgen.py --ip 192.168.1.100 --port 4444 --lang bash"
echo "  ./revgen.py --ip 192.168.1.100 --port 4444 --all"
echo ""
echo "Run the demo:"
echo "  ./demo.py"
echo ""
echo "Remember: Use only on systems you own or have permission to test! 🔒"
