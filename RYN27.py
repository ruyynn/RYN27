#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 Recon Tool - Ultimate Information Gathering
Version 1.0.0 - early version
Coded by: Ruyynn
GitHub: https://github.com/ruyynn
"""

import os
import sys
import time
import socket
import subprocess
import json
import re
from urllib.parse import urlparse
from datetime import datetime

# Auto-install dependencies
required_packages = {
    'requests': 'requests',
    'rich': 'rich',
    'python-whois': 'whois',
    'dnspython': 'dns',
    'builtwith': 'builtwith',
    'beautifulsoup4': 'bs4'
}

missing = []
for pkg, import_name in required_packages.items():
    try:
        __import__(import_name)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"[!] Missing dependencies: {', '.join(missing)}")
    print("[*] Installing...")
    for pkg in missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--break-system-packages"])
    print("[*] Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.columns import Columns
from rich.text import Text
from rich.theme import Theme
import whois
import dns.resolver
import dns.zone
import dns.query
import dns.name
import builtwith
from bs4 import BeautifulSoup

# ============================================================
# CROSS-PLATFORM COLOR DETECTION & THEME
# ============================================================

def detect_color_support():
    """
    Detect terminal color capability across Linux, Windows, macOS, Termux.
    Returns: 'truecolor', '256', 'basic', or 'none'
    """
    # Windows: enable VT100 via ctypes
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
        # Windows Terminal & newer cmd support truecolor
        if os.environ.get("WT_SESSION") or os.environ.get("COLORTERM") in ("truecolor", "24bit"):
            return "truecolor"
        return "256"

    # Check COLORTERM env (most modern terminals set this)
    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return "truecolor"

    # Check TERM_PROGRAM (macOS Terminal, iTerm2, etc.)
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    if term_program in ("iterm.app", "hyper", "vscode", "wezterm"):
        return "truecolor"
    if term_program == "apple_terminal":
        return "256"

    # Check TERM variable
    term = os.environ.get("TERM", "").lower()
    if "256color" in term or "256colour" in term:
        return "256"
    if term in ("xterm", "screen", "tmux"):
        return "256"

    # Termux sets PREFIX, also usually supports 256
    if os.environ.get("PREFIX") and "com.termux" in os.environ.get("PREFIX", ""):
        return "256"

    # CI / no TTY
    if not sys.stdout.isatty():
        return "none"

    return "256"  # safe default


COLOR_LEVEL = detect_color_support()

# ============================================================
# THEME — degrades gracefully per color level
# ============================================================

if COLOR_LEVEL == "truecolor":
    # Full RGB — deep jewel tones
    THEME = Theme({
        "primary":      "bold #00D4FF",   # electric cyan
        "secondary":    "bold #BF5FFF",   # vivid violet
        "accent":       "bold #00FF9F",   # neon mint
        "warning":      "bold #FFD700",   # gold
        "danger":       "bold #FF4560",   # crimson
        "muted":        "#6C7A89",        # slate grey
        "success":      "bold #00E676",   # emerald
        "title":        "bold #FF6B9D",   # hot pink
        "border":       "#00D4FF",
        "label":        "bold #E0E0E0",
        "value":        "#B0BEC5",
        "logo1":        "bold #FF2020",   # merah
        "logo2":        "bold #FFFFFF",   # putih
        "logo3":        "bold #FF2020",   # merah
        "logo4":        "bold #FFFFFF",   # putih
        "logo5":        "bold #FF2020",   # merah
        "logo6":        "bold #FFFFFF",   # putih
        "logo7":        "bold #FF2020",   # merah
        "star":         "bold #FFD700",   # kuning emas
    })
    BORDER_STYLE   = "#00D4FF"
    PANEL_BORDER   = "#BF5FFF"
    TITLE_STYLE    = "bold #FF6B9D"
    MENU_OPT_STYLE = "bold #FFD700"
    MENU_FN_STYLE  = "bold #E0E0E0"
    PROMPT_STYLE   = "bold #FFD700"
    INPUT_STYLE    = "bold #00D4FF"
    EXIT_STYLE     = "bold #00E676"
    LOGO_COLORS    = ["logo1","logo2","logo3","logo4","logo5","logo6","logo7"]

elif COLOR_LEVEL == "256":
    # 256-color palette — vivid but safe
    THEME = Theme({
        "primary":      "bold cyan",
        "secondary":    "bold magenta",
        "accent":       "bold green",
        "warning":      "bold yellow",
        "danger":       "bold red",
        "muted":        "bright_black",
        "success":      "bold bright_green",
        "title":        "bold bright_magenta",
        "border":       "cyan",
        "label":        "bold white",
        "value":        "bright_white",
        "logo1":        "bold red",
        "logo2":        "bold white",
        "logo3":        "bold red",
        "logo4":        "bold white",
        "logo5":        "bold red",
        "logo6":        "bold white",
        "logo7":        "bold red",
        "star":         "bold yellow",
    })
    BORDER_STYLE   = "cyan"
    PANEL_BORDER   = "magenta"
    TITLE_STYLE    = "bold bright_magenta"
    MENU_OPT_STYLE = "bold bright_yellow"
    MENU_FN_STYLE  = "bold white"
    PROMPT_STYLE   = "bold bright_yellow"
    INPUT_STYLE    = "bold cyan"
    EXIT_STYLE     = "bold bright_green"
    LOGO_COLORS    = ["logo1","logo2","logo3","logo4","logo5","logo6","logo7"]

else:
    # Basic / no color — clean monochrome, still structured
    THEME = Theme({
        "primary":   "bold",
        "secondary": "bold",
        "accent":    "bold",
        "warning":   "bold",
        "danger":    "bold",
        "muted":     "",
        "success":   "bold",
        "title":     "bold",
        "border":    "white",
        "label":     "bold",
        "value":     "",
        "logo1": "bold", "logo2": "bold", "logo3": "bold",
        "logo4": "bold", "logo5": "bold", "logo6": "bold", "logo7": "bold",
        "star":  "bold",
    })
    BORDER_STYLE   = "white"
    PANEL_BORDER   = "white"
    TITLE_STYLE    = "bold"
    MENU_OPT_STYLE = "bold"
    MENU_FN_STYLE  = "bold"
    PROMPT_STYLE   = "bold"
    INPUT_STYLE    = "bold"
    EXIT_STYLE     = "bold"
    LOGO_COLORS    = ["logo1"] * 7


# Inisialisasi console dengan theme
console = Console(theme=THEME)

# ============================================================
# LOGO UTAMA RYN27
# ============================================================

LOGO_MAIN = r"""
 ███████████   █████ █████ ██████   █████  ████████  ██████████
 ░░███░░░░░███ ░░███ ░░███ ░░██████ ░░███  ███░░░░███░███░░░░███
  ░███    ░███  ░░███ ███   ░███░███ ░███ ░░░    ░███░░░    ███ 
  ░██████████    ░░█████    ░███░░███░███    ███████       ███  
  ░███░░░░░███    ░░███     ░███ ░░██████   ███░░░░       ███   
  ░███    ░███     ░███     ░███  ░░█████  ███      █    ███    
  █████   █████    █████    █████  ░░█████░██████████   ███     
 ░░░░░   ░░░░░    ░░░░░    ░░░░░    ░░░░░ ░░░░░░░░░░   ░░░      
"""

def print_gradient_logo():
    """Cetak logo seperti bendera Indonesia - merah atas, putih bawah"""
    lines = LOGO_MAIN.split('\n')
    # Hanya baris berisi konten 
    content_lines = [l for l in lines if l.strip()]
    total = len(content_lines)
    half = total // 2

    for idx, line in enumerate(content_lines):
        if idx < half:
            # Setengah atas — MERAH
            if COLOR_LEVEL == "truecolor":
                console.print(f"[bold #CE1126]{line}[/bold #CE1126]")
            elif COLOR_LEVEL == "256":
                console.print(f"[bold red]{line}[/bold red]")
            else:
                console.print(f"[bold]{line}[/bold]")
        else:
            # Setengah bawah — PUTIH
            if COLOR_LEVEL == "truecolor":
                console.print(f"[bold #FFFFFF]{line}[/bold #FFFFFF]")
            elif COLOR_LEVEL == "256":
                console.print(f"[bold white]{line}[/bold white]")
            else:
                console.print(f"[bold]{line}[/bold]")

# ============================================================
# LOGO - TERMINAL STYLE
# ============================================================

NEW_LOGO = r"""
                *          /                \
               * *        /   give a star    \
              *   *     / \  for this tool   /
             * O O *   /   \                /
            *   |   *
* * * * * *   \   /   * * * * * *
  *            \ /            *
     *                     *
        *               *
          *     *     *
         *    *   *    *
        *   *       *   *
       *  *           *  *
      * *               * *
     *                     *

"""

# ============================================================
# FUNGSI UTAMA
# ============================================================

def get_ip_from_domain(domain):
    """Resolve domain ke IP (A record)"""
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def print_result(title, data):
    """Tampilkan hasil dalam panel premium"""
    panel = Panel(
        data,
        title=f"[{TITLE_STYLE}]{title}[/{TITLE_STYLE}]",
        border_style=PANEL_BORDER,
        title_align="left",
        padding=(1, 2)
    )
    console.print(panel)

# 1. Website Information
def website_info(url):
    """Ambil informasi HTTP header, status, title, cookies"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        start = time.time()
        r = requests.get(url, timeout=15, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
        elapsed = time.time() - start
        info = f"[label]URL:[/label] {r.url}\n"
        info += f"[label]Status Code:[/label] {r.status_code}\n"
        info += f"[label]Response Time:[/label] {elapsed:.2f}s\n"
        info += f"[label]Server:[/label] {r.headers.get('Server', 'N/A')}\n"
        info += f"[label]Content-Type:[/label] {r.headers.get('Content-Type', 'N/A')}\n"
        info += f"[label]Cookies:[/label] {len(r.cookies)}\n"
        # Title
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title')
        info += f"[label]Title:[/label] {title.text if title else 'N/A'}\n"
        # Headers
        info += "\n[label]HTTP Headers:[/label]\n"
        for h, v in r.headers.items():
            info += f"  [accent]{h}:[/accent] {v}\n"
        print_result("Website Information", info)
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 2. Domain Whois Lookup
def domain_whois(domain):
    """WHOIS lookup menggunakan library whois"""
    try:
        w = whois.whois(domain)
        info = f"[label]Domain:[/label] {w.domain_name}\n"
        info += f"[label]Registrar:[/label] {w.registrar}\n"
        info += f"[label]Creation Date:[/label] {w.creation_date}\n"
        info += f"[label]Expiration Date:[/label] {w.expiration_date}\n"
        info += f"[label]Name Servers:[/label] {', '.join(w.name_servers) if w.name_servers else 'N/A'}\n"
        info += f"[label]Status:[/label] {w.status}\n"
        info += f"[label]Emails:[/label] {w.emails}\n"
        info += f"[label]Organization:[/label] {w.org}\n"
        info += f"[label]Country:[/label] {w.country}\n"
        print_result("Domain Whois", info)
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 3. Find IP Location (menggunakan ip-api.com)
def ip_location(target):
    """Cari lokasi geografis IP (kota, negara, ISP)"""
    try:
        ip = target
        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
            ip = socket.gethostbyname(target)
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success':
                info = f"[label]IP:[/label] {data['query']}\n"
                info += f"[label]Country:[/label] {data['country']}\n"
                info += f"[label]Region:[/label] {data['regionName']}\n"
                info += f"[label]City:[/label] {data['city']}\n"
                info += f"[label]ZIP:[/label] {data.get('zip', 'N/A')}\n"
                info += f"[label]Lat/Lon:[/label] {data['lat']}, {data['lon']}\n"
                info += f"[label]ISP:[/label] {data['isp']}\n"
                info += f"[label]Organization:[/label] {data['org']}\n"
                info += f"[label]AS:[/label] {data['as']}\n"
                print_result("IP Location", info)
            else:
                console.print(f"[danger]Error: {data.get('message', 'Unknown error')}[/danger]")
        else:
            console.print("[danger]Failed to reach ip-api.com[/danger]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 4. Recommended Port Scan
def port_scan(host):
    """Scan port umum (TCP connect)"""
    ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443]
    open_ports = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("[primary]Scanning ports...", total=len(ports))
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, 'tcp')
                except:
                    service = "unknown"
                open_ports.append((port, service))
            sock.close()
            progress.update(task, advance=1)
    if open_ports:
        info = f"[label]Open ports on {host}:[/label]\n"
        for port, service in open_ports:
            info += f"  [success]●[/success] [accent]{port}/tcp[/accent] ({service}) - [success]open[/success]\n"
    else:
        info = "[warning]No open ports found on common ports.[/warning]"
    print_result("Port Scan", info)

# 5. DNS Whois Lookup (sama dengan domain whois)
def dns_whois(domain):
    domain_whois(domain)

# 7. DNS Zone Transfers Lookup
def zone_transfer(domain):
    """Coba lakukan zone transfer ke semua nameserver"""
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        for ns in ns_records:
            ns_name = str(ns)
            try:
                ns_ip = dns.resolver.resolve(ns_name, 'A')[0].to_text()
                console.print(f"[muted]Trying zone transfer from {ns_name} ({ns_ip})...[/muted]")
                zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=10, lifetime=15))
                if zone:
                    info = f"[label]Zone transfer successful from {ns_name} ({ns_ip}):[/label]\n"
                    for name, node in zone.nodes.items():
                        rdatasets = node.rdatasets
                        for rdataset in rdatasets:
                            for rdata in rdataset:
                                info += f"[accent]{name}[/accent] {rdataset.ttl} {rdataset.rdtype} {rdata}\n"
                    print_result("Zone Transfer", info)
                    return
            except Exception as e:
                console.print(f"[muted]Failed: {e}[/muted]")
                continue
        console.print("[warning]Zone transfer failed on all nameservers.[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 8. Reverse IP Lookup (gunakan hackertarget)
def reverse_ip(ip):
    """Cari domain yang menggunakan IP yang sama"""
    try:
        r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=15)
        if r.status_code == 200:
            data = r.text.strip()
            if data and "error" not in data.lower() and "API count" not in data.lower():
                info = f"[label]Domains hosted on {ip}:[/label]\n[value]{data}[/value]"
                print_result("Reverse IP", info)
            else:
                console.print("[warning]No domains found or API limit reached.[/warning]")
        else:
            console.print("[danger]API error[/danger]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 9. Forward IP Lookup
def forward_ip(domain):
    ip = get_ip_from_domain(domain)
    if ip:
        print_result("Forward IP", f"[label]{domain}[/label] [muted]→[/muted] [primary]{ip}[/primary]")
    else:
        console.print("[danger]Could not resolve domain[/danger]")

# 10. Reverse DNS Lookup
def reverse_dns(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        print_result("Reverse DNS", f"[label]{ip}[/label] [muted]→[/muted] [primary]{host}[/primary]")
    except:
        console.print("[danger]No PTR record found[/danger]")

# 11. Forward DNS Lookup (A record)
def forward_dns(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        info = f"[label]A records for {domain}:[/label]\n"
        for rdata in answers:
            info += f"  [success]●[/success] [primary]{rdata.address}[/primary]\n"
        print_result("Forward DNS", info)
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 12. Shared DNS Lookup (gunakan hackertarget)
def shared_dns(domain):
    try:
        r = requests.get(f"https://api.hackertarget.com/findshareddns/?q={domain}", timeout=15)
        if r.status_code == 200:
            data = r.text.strip()
            if data and "error" not in data.lower() and "API count" not in data.lower():
                info = f"[label]Domains sharing DNS with {domain}:[/label]\n[value]{data}[/value]"
                print_result("Shared DNS", info)
            else:
                console.print("[warning]No shared domains found or API limit reached.[/warning]")
        else:
            console.print("[danger]API error[/danger]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 13. Technology lookup
def tech_lookup(url):
    """Deteksi teknologi menggunakan builtwith"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        tech = builtwith.parse(url)
        if tech:
            info = ""
            for cat, val in tech.items():
                info += f"[accent]{cat}:[/accent] [value]{', '.join(val)}[/value]\n"
            print_result("Technology Lookup", info)
        else:
            console.print("[warning]No technologies detected[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# 14. Website Recon (gabungan info + teknologi)
def website_recon(url):
    website_info(url)
    tech_lookup(url)

# 15. Metadata Crawler
def metadata_crawler(url):
    """Ambil semua meta tags dari halaman"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        metas = soup.find_all('meta')
        if metas:
            info = ""
            for meta in metas:
                if meta.get('name'):
                    info += f"[accent]name[/accent]=[value]'{meta['name']}'[/value] [label]content[/label]='{meta.get('content', '')}'\n"
                elif meta.get('property'):
                    info += f"[accent]property[/accent]=[value]'{meta['property']}'[/value] [label]content[/label]='{meta.get('content', '')}'\n"
                elif meta.get('http-equiv'):
                    info += f"[accent]http-equiv[/accent]=[value]'{meta['http-equiv']}'[/value] [label]content[/label]='{meta.get('content', '')}'\n"
                else:
                    info += f"[muted]{meta}[/muted]\n"
            print_result("Metadata Crawler", info)
        else:
            console.print("[warning]No meta tags found[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")

# ============================================================
# MENU UTAMA DENGAN LOGO BARU DI DALAM BOX
# ============================================================

def create_premium_menu():
    """Buat menu table dengan gaya premium"""
    menu_table = Table(show_header=False, box=box.ROUNDED, border_style=BORDER_STYLE, pad_edge=True)
    menu_table.add_column("Option", style=MENU_OPT_STYLE, width=6)
    menu_table.add_column("Function", style=MENU_FN_STYLE, width=50)

    options = [
        ("[1]", "Website Information"),
        ("[2]", "Domain Whois Lookup"),
        ("[3]", "Find IP Location"),
        ("[4]", "Recommended Port Scan"),
        ("[5]", "DNS Whois Lookup"),
        ("[7]", "DNS Zone Transfers Lookup"),
        ("[8]", "Reverse IP Lookup"),
        ("[9]", "Forward IP Lookup"),
        ("[10]", "Reverse DNS Lookup"),
        ("[11]", "Forward DNS Lookup"),
        ("[12]", "Shared DNS Lookup"),
        ("[13]", "Technology lookup"),
        ("[14]", "Website Recon"),
        ("[15]", "Metadata Crawler"),
        ("[0]", "Exit"),
    ]
    for opt, desc in options:
        menu_table.add_row(opt, desc)

    return menu_table

def show_menu():
    """Tampilkan menu dengan logo baru di dalam box (sebelah kanan)"""
    menu_table = create_premium_menu()
    logo_text = Text(NEW_LOGO, style="star")

    # Gabungkan menu dan logo dalam dua kolom
    columns = Columns([menu_table, logo_text], equal=False, expand=True)

    # Bungkus dalam panel utama
    main_panel = Panel(
        columns,
        title=f"[{TITLE_STYLE}]⚡ RYN27 RECON MENU ⚡[/{TITLE_STYLE}]",
        border_style=PANEL_BORDER,
        title_align="center",
        padding=(1, 2)
    )
    console.print(main_panel)

def main():
    console.clear()
    print_gradient_logo()
    console.print(f"\n[primary]🔍 Follow me on GitHub: [secondary]@ruyynn[/secondary] 🔍[/primary]\n")

    while True:
        show_menu()
        choice = Prompt.ask(f"[{PROMPT_STYLE}]➤ Choose option[/{PROMPT_STYLE}]")

        if choice == "0":
            console.print(f"\n[{EXIT_STYLE}]Exiting... Stay safe![/{EXIT_STYLE}]")
            break

        # Untuk opsi yang membutuhkan URL/domain
        if choice in ["1","2","5","14","15"]:
            target = Prompt.ask(f"[{INPUT_STYLE}]Enter target URL/domain[/{INPUT_STYLE}]")
            if choice == "1":
                website_info(target)
            elif choice == "2":
                domain_whois(target)
            elif choice == "5":
                dns_whois(target)
            elif choice == "14":
                website_recon(target)
            elif choice == "15":
                metadata_crawler(target)

        # Opsi yang bisa menerima IP atau domain
        elif choice in ["3","4","8","10"]:
            target = Prompt.ask(f"[{INPUT_STYLE}]Enter target IP or domain[/{INPUT_STYLE}]")
            if choice == "3":
                ip_location(target)
            elif choice == "4":
                ip = get_ip_from_domain(target) if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target) else target
                if ip:
                    port_scan(ip)
                else:
                    console.print("[danger]Invalid target[/danger]")
            elif choice == "8":
                ip = get_ip_from_domain(target) if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target) else target
                if ip:
                    reverse_ip(ip)
                else:
                    console.print("[danger]Invalid target[/danger]")
            elif choice == "10":
                ip = get_ip_from_domain(target) if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target) else target
                if ip:
                    reverse_dns(ip)
                else:
                    console.print("[danger]Invalid target[/danger]")

        # Opsi yang hanya domain
        elif choice in ["7","9","11","12","13"]:
            domain = Prompt.ask(f"[{INPUT_STYLE}]Enter domain[/{INPUT_STYLE}]")
            if choice == "7":
                zone_transfer(domain)
            elif choice == "9":
                forward_ip(domain)
            elif choice == "11":
                forward_dns(domain)
            elif choice == "12":
                shared_dns(domain)
            elif choice == "13":
                tech_lookup(domain)

        else:
            console.print("[danger]Invalid option[/danger]")

        input("\nPress Enter to continue...")
        console.clear()
        print_gradient_logo()
        console.print(f"\n[primary]🔍 Follow me on GitHub: [secondary]@ruyynn[/secondary] 🔍[/primary]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[warning]Interrupted by user[/warning]")
        sys.exit(0)