#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 Recon Tool — Ultimate Information Gathering
Version 1.8.0
Coded by: Ruyynn
GitHub  : https://github.com/ruyynn/RYN27

Entry point — handles dependency installation then launches the
interactive menu. All feature logic lives in modules/.
"""

import os
import sys
import subprocess

# ============================================================
# AUTO-INSTALL DEPENDENCIES (runs before any rich import)
# ============================================================

REQUIRED_PACKAGES = {
    "requests":      "requests",
    "rich":          "rich",
    "python-whois":  "whois",
    "dnspython":     "dns",
    "builtwith":     "builtwith",
    "beautifulsoup4":"bs4",
    "cryptography":  "cryptography",
}

missing = []
for pkg, import_name in REQUIRED_PACKAGES.items():
    try:
        __import__(import_name)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"[!] Missing: {', '.join(missing)}")
    print("[*] Installing dependencies — please wait...")
    for pkg in missing:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg,
             "--break-system-packages", "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    print("[*] Done! Restarting RYN27...\n")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# ============================================================
# MAIN IMPORTS (safe after dependency check)
# ============================================================

from rich.prompt import Prompt

from modules.theme    import console, EXIT_STYLE, PROMPT_STYLE, INPUT_STYLE
from modules.logo     import print_header
from modules.menu     import show_menu, show_tutorial, show_about, show_star_cta
from modules.utils    import VERSION

# Feature imports
from modules.web_recon import (
    website_info,
    header_security_audit,
    tech_lookup,
    metadata_crawler,
    robots_sitemap,
    email_harvester,
    website_recon,
)
from modules.dns_tools import (
    dns_records,
    domain_whois,
    subdomain_enum,
    zone_transfer,
    shared_dns,
    forward_dns,
)
from modules.ip_tools import (
    ip_location,
    port_scan,
    reverse_ip,
    forward_ip,
    reverse_dns,
    ssl_info,
)

# ============================================================
# DISPATCH TABLE
# ============================================================

# Maps menu option → (function, prompt_message)
DISPATCH: dict[str, tuple] = {
    # Web Recon
    "1":  (website_info,           "Enter target URL/domain"),
    "2":  (header_security_audit,  "Enter target URL/domain"),
    "3":  (tech_lookup,            "Enter target URL/domain"),
    "4":  (metadata_crawler,       "Enter target URL/domain"),
    "5":  (robots_sitemap,         "Enter target URL/domain"),
    "6":  (email_harvester,        "Enter target URL/domain"),
    "7":  (website_recon,          "Enter target URL/domain"),
    # DNS / Network
    "8":  (dns_records,            "Enter domain"),
    "9":  (domain_whois,           "Enter domain"),
    "10": (subdomain_enum,         "Enter domain"),
    "11": (zone_transfer,          "Enter domain"),
    "12": (shared_dns,             "Enter domain"),
    "13": (forward_dns,            "Enter domain"),
    # IP / Host
    "14": (ip_location,            "Enter IP or domain"),
    "15": (port_scan,              "Enter IP or domain"),
    "16": (reverse_ip,             "Enter IP or domain"),
    "17": (forward_ip,             "Enter domain"),
    "18": (reverse_dns,            "Enter IP or domain"),
    # SSL
    "19": (ssl_info,               "Enter domain (e.g. example.com)"),
}

# No-input options (menus / info pages)
INFO_OPTIONS = {
    "20": show_tutorial,
    "21": show_about,
    "22": show_star_cta,
}

# ============================================================
# MAIN LOOP
# ============================================================

def main() -> None:
    console.clear()
    print_header()

    while True:
        show_menu()
        choice = Prompt.ask(
            f"[{PROMPT_STYLE}]➤  Choose option[/{PROMPT_STYLE}]"
        ).strip()

        # Exit
        if choice == "0":
            console.print(
                f"\n[{EXIT_STYLE}]  ✔  Exiting RYN27 v{VERSION}..."
                f"  Stay safe & hack responsibly!  🇮🇩  [/{EXIT_STYLE}]"
            )
            console.print()
            sys.exit(0)

        # Info / no-input pages
        if choice in INFO_OPTIONS:
            console.print()
            INFO_OPTIONS[choice]()

        # Feature options
        elif choice in DISPATCH:
            fn, prompt_msg = DISPATCH[choice]
            console.print()
            target = Prompt.ask(
                f"[{INPUT_STYLE}]➤  {prompt_msg}[/{INPUT_STYLE}]"
            ).strip()
            if not target:
                console.print("[warning]Empty input — please enter a valid target.[/warning]")
            else:
                console.print()
                fn(target)

        else:
            console.print(
                "[danger]Invalid option — enter a number from the menu above.[/danger]"
            )

        # Pause before redraw
        console.print()
        Prompt.ask(
            f"[muted]Press Enter to return to menu[/muted]",
            default="",
            show_default=False,
        )
        console.clear()
        print_header()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[warning]  Interrupted by user — Goodbye! 👋[/warning]")
        sys.exit(0)
