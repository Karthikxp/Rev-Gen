#!/usr/bin/env python3
"""
Reverse Shell Payload Generator
Handles template processing and payload generation logic
"""

import json
import os
import re
import ipaddress
from typing import Dict, List, Optional, Tuple


class PayloadGenerator:
    """Main payload generator class"""
    
    def __init__(self, shells_file: str = "shells.json"):
        """Initialize generator with shells database"""
        self.shells_file = shells_file
        self.shells_data = self._load_shells()
    
    def _load_shells(self) -> Dict:
        """Load shell payloads from JSON file"""
        try:
            # Try current directory first, then script directory
            if os.path.exists(self.shells_file):
                filepath = self.shells_file
            else:
                script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                filepath = os.path.join(script_dir, self.shells_file)
            
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Shells database not found: {self.shells_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in shells database: {e}")
    
    def is_ipv6(self, ip: str) -> bool:
        """Check if IP address is IPv6"""
        try:
            addr = ipaddress.ip_address(ip)
            return isinstance(addr, ipaddress.IPv6Address)
        except ValueError:
            return False
    
    def get_available_shells(self) -> List[str]:
        """Get list of available shell types"""
        shells = list(self.shells_data.get("shells", {}).keys())
        persistent_shells = [f"{shell}_persistent" for shell in self.shells_data.get("persistent_shells", {}).keys()]
        return shells + persistent_shells
    
    def get_shell_info(self, shell_type: str) -> Optional[Dict]:
        """Get information about a specific shell type"""
        shells = self.shells_data.get("shells", {})
        ipv6_shells = self.shells_data.get("ipv6_shells", {})
        persistent_shells = self.shells_data.get("persistent_shells", {})
        
        # Handle persistent shell types
        if shell_type.endswith("_persistent"):
            base_shell = shell_type[:-11]  # Remove "_persistent" suffix
            if base_shell in persistent_shells:
                return persistent_shells[base_shell]
        
        if shell_type in shells:
            return shells[shell_type]
        elif shell_type in ipv6_shells:
            return ipv6_shells[shell_type]
        elif shell_type in persistent_shells:
            return persistent_shells[shell_type]
        else:
            return None
    
    def generate_payload(self, ip: str, port: int, shell_type: str) -> Tuple[str, Dict]:
        """
        Generate a reverse shell payload
        Returns: (payload_string, shell_info)
        """
        # Validate inputs
        if not self._validate_ip(ip):
            raise ValueError(f"Invalid IP address: {ip}")
        
        if not self._validate_port(port):
            raise ValueError(f"Invalid port: {port}. Must be 1-65535")
        
        # Determine if IPv6 and get appropriate shell database
        is_ipv6 = self.is_ipv6(ip)
        
        # Handle persistent shell types
        if shell_type.endswith("_persistent"):
            base_shell = shell_type[:-11]  # Remove "_persistent" suffix
            shells_db = self.shells_data.get("persistent_shells", {})
            if base_shell not in shells_db:
                available = ", ".join(self.get_available_shells())
                raise ValueError(f"Unknown persistent shell type: {shell_type}. Available: {available}")
            shell_info = shells_db[base_shell]
        else:
            if is_ipv6:
                shells_db = self.shells_data.get("ipv6_shells", {})
                # Fallback to regular shells if IPv6 version not available
                if shell_type not in shells_db:
                    shells_db = self.shells_data.get("shells", {})
            else:
                shells_db = self.shells_data.get("shells", {})
            
            # Get shell template
            if shell_type not in shells_db:
                available = ", ".join(self.get_available_shells())
                raise ValueError(f"Unknown shell type: {shell_type}. Available: {available}")
            
            shell_info = shells_db[shell_type]
        template = shell_info["payload"]
        
        # Format the payload with IP and port
        try:
            payload = template.format(ip=ip, port=port)
            return payload, shell_info
        except KeyError as e:
            raise ValueError(f"Template error in {shell_type}: missing placeholder {e}")
    
    def generate_all_payloads(self, ip: str, port: int) -> Dict[str, Tuple[str, Dict]]:
        """Generate payloads for all available shell types"""
        results = {}
        available_shells = self.get_available_shells()
        
        for shell_type in available_shells:
            try:
                payload, info = self.generate_payload(ip, port, shell_type)
                results[shell_type] = (payload, info)
            except Exception as e:
                # Skip shells that fail to generate
                results[shell_type] = (f"Error: {str(e)}", {"name": shell_type, "error": True})
        
        return results
    
    def _validate_ip(self, address: str) -> bool:
        """Validate IP address or hostname format"""
        # First, check for valid IP address
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            # If not an IP, check if it's a resolvable hostname
            try:
                import socket
                socket.gethostbyname(address)
                return True
            except socket.gaierror:
                return False
    
    def _validate_port(self, port: int) -> bool:
        """Validate port number"""
        return isinstance(port, int) and 1 <= port <= 65535
    
    def get_payload_stats(self) -> Dict:
        """Get statistics about available payloads"""
        shells = self.shells_data.get("shells", {})
        ipv6_shells = self.shells_data.get("ipv6_shells", {})
        
        return {
            "total_shells": len(shells),
            "ipv6_shells": len(ipv6_shells),
            "languages": list(shells.keys()),
            "ipv6_languages": list(ipv6_shells.keys())
        }


# Utility functions for external use
def quick_generate(ip: str, port: int, shell_type: str, shells_file: str = "shells.json") -> str:
    """Quick payload generation function"""
    generator = PayloadGenerator(shells_file)
    payload, _ = generator.generate_payload(ip, port, shell_type)
    return payload


def list_shells(shells_file: str = "shells.json") -> List[str]:
    """Quick function to list available shells"""
    generator = PayloadGenerator(shells_file)
    return generator.get_available_shells()


if __name__ == "__main__":
    # Test the generator
    gen = PayloadGenerator()
    print("Available shells:", gen.get_available_shells())
    
    # Test payload generation
    try:
        payload, info = gen.generate_payload("192.168.1.100", 4444, "bash")
        print(f"\nTest payload ({info['name']}): {payload}")
    except Exception as e:
        print(f"Error: {e}")
