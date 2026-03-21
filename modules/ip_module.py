#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/ip_module.py
IP & host features: geolocation, threaded port scan,
reverse IP, forward IP, reverse DNS.
"""

import socket
import threading
import concurrent.futures

import requests
from rich import box
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from modules.core import (
    console, clean_domain, get_ip_from_domain, is_ip,
    print_result, section, spinner,
    BORDER_STYLE, MENU_OPT_STYLE
)


# ─────────────────────────────────────────────────────────────────────────────
# 14. IP GEOLOCATION
# ─────────────────────────────────────────────────────────────────────────────

def ip_location(target: str):
    """Geolocate an IP or domain: country, city, ISP, ASN, proxy/VPN flags."""
    target = clean_domain(target)
    try:
        ip = target if is_ip(target) else socket.gethostbyname(target)

        with spinner(f"Geolocating {ip}...") as p:
            p.add_task("geo")
            r = requests.get(
                f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,"
                f"regionName,city,zip,lat,lon,isp,org,as,asname,mobile,proxy,hosting,query",
                timeout=10,
            )
        data = r.json()
        if data.get("status") != "success":
            console.print(f"[danger]Error: {data.get('message', 'Unknown error')}[/danger]")
            return

        cc   = data.get("countryCode", "")
        flag = "".join(chr(0x1F1E0 + ord(c) - ord("A")) for c in cc) if len(cc) == 2 else ""

        info  = section("Location")
        info += f"[label]IP Address   :[/label] [primary]{data['query']}[/primary]\n"
        info += f"[label]Country      :[/label] [value]{flag} {data['country']} ({cc})[/value]\n"
        info += f"[label]Region       :[/label] [value]{data['regionName']}[/value]\n"
        info += f"[label]City         :[/label] [value]{data['city']}[/value]\n"
        info += f"[label]ZIP          :[/label] [value]{data.get('zip', 'N/A')}[/value]\n"
        info += f"[label]Coordinates  :[/label] [accent]{data['lat']}, {data['lon']}[/accent]\n"
        info += (
            f"[label]Maps Link    :[/label] [muted]"
            f"https://maps.google.com/?q={data['lat']},{data['lon']}[/muted]\n"
        )

        info += section("Network")
        info += f"[label]ISP          :[/label] [value]{data['isp']}[/value]\n"
        info += f"[label]Organization :[/label] [value]{data['org']}[/value]\n"
        info += f"[label]AS Number    :[/label] [value]{data['as']}[/value]\n"
        info += f"[label]AS Name      :[/label] [value]{data.get('asname', 'N/A')}[/value]\n"

        info += section("Flags")
        mobile  = "[open]YES[/open]" if data.get("mobile") else "[closed]NO[/closed]"
        proxy   = "[danger]YES — PROXY/VPN DETECTED[/danger]" if data.get("proxy") else "[open]NO[/open]"
        hosting = "[warning]YES[/warning]" if data.get("hosting") else "[open]NO[/open]"
        info += f"[label]Mobile       :[/label] {mobile}\n"
        info += f"[label]Proxy / VPN  :[/label] {proxy}\n"
        info += f"[label]Hosting      :[/label] {hosting}\n"

        print_result("IP Geolocation", info, subtitle=ip)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 15. PORT SCAN (THREADED + BANNER GRAB)
# ─────────────────────────────────────────────────────────────────────────────

COMMON_PORTS = {
    21: "FTP",         22: "SSH",          23: "Telnet",
    25: "SMTP",        53: "DNS",           80: "HTTP",
    110: "POP3",       111: "RPC",         135: "MSRPC",
    139: "NetBIOS",    143: "IMAP",        443: "HTTPS",
    445: "SMB",        465: "SMTPS",       587: "SMTP-TLS",
    993: "IMAPS",      995: "POP3S",       1433: "MSSQL",
    1723: "PPTP",      3306: "MySQL",      3389: "RDP",
    5432: "PostgreSQL",5900: "VNC",        6379: "Redis",
    8080: "HTTP-Alt",  8443: "HTTPS-Alt",  8888: "HTTP-Alt2",
    27017: "MongoDB",
}

def _scan_port(host: str, port: int, timeout: float = 1.2):
    """Scan a single TCP port and attempt a quick banner grab."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        banner = ""
        if result == 0:
            try:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                sock.settimeout(0.8)
                raw   = sock.recv(256).decode("utf-8", errors="ignore").strip()
                first = raw.split("\n")[0].strip()
                if first:
                    banner = first[:80]
            except Exception:
                pass
        sock.close()
        return result == 0, banner
    except Exception:
        return False, ""

def port_scan(host: str):
    """Threaded TCP connect scan across COMMON_PORTS with banner grabbing."""
    host = clean_domain(host)
    if not is_ip(host):
        ip = get_ip_from_domain(host)
        if not ip:
            console.print("[danger]Cannot resolve host to IP[/danger]")
            return
        host = ip

    console.print(
        f"\n[primary]Scanning [accent]{host}[/accent] — {len(COMMON_PORTS)} ports[/primary]\n"
    )

    open_ports: list = []
    lock = threading.Lock()

    with Progress(
        SpinnerColumn(style="primary"),
        TextColumn("[primary]Scanning port {task.fields[port]}[/primary]"),
        BarColumn(bar_width=35, style="primary"),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("scan", total=len(COMMON_PORTS), port="...")

        def check(port: int):
            progress.update(task, advance=1, port=str(port))
            ok, banner = _scan_port(host, port)
            if ok:
                service = COMMON_PORTS.get(port, "unknown")
                with lock:
                    open_ports.append((port, service, banner))

        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            ex.map(check, COMMON_PORTS.keys())

    open_ports.sort(key=lambda x: x[0])

    if open_ports:
        t = Table(
            show_header=True, box=box.SIMPLE_HEAD,
            border_style=BORDER_STYLE, header_style=MENU_OPT_STYLE,
        )
        t.add_column("Port",    style="accent",  width=8)
        t.add_column("Service", style="value",   width=14)
        t.add_column("State",   style="open",    width=8)
        t.add_column("Banner",  style="muted")
        for port, svc, banner in open_ports:
            t.add_row(str(port), svc, "OPEN", banner or "—")

        print_result("Port Scan", f"[open]Found {len(open_ports)} open port(s) on {host}[/open]")
        console.print(t)
    else:
        print_result("Port Scan",
                     f"[warning]No open ports found on {host} from the {len(COMMON_PORTS)}-port list.[/warning]")


# ─────────────────────────────────────────────────────────────────────────────
# 16. REVERSE IP LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

def reverse_ip(target: str):
    """Find domains hosted on the same IP (via HackerTarget API)."""
    target = clean_domain(target)
    ip     = target if is_ip(target) else get_ip_from_domain(target)
    if not ip:
        console.print("[danger]Cannot resolve host to IP[/danger]")
        return
    try:
        with spinner(f"Reverse IP lookup for {ip}...") as p:
            p.add_task("rip")
            r = requests.get(
                f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=15
            )
        data = r.text.strip()
        if data and "error" not in data.lower() and "API count" not in data.lower():
            domains = [d.strip() for d in data.split("\n") if d.strip()]
            info    = f"[open]Found {len(domains)} domain(s) on {ip}[/open]\n\n"
            for d in domains:
                info += f"  [accent]◆[/accent] [value]{d}[/value]\n"
            print_result("Reverse IP Lookup", info, subtitle=ip)
        else:
            console.print("[warning]No results or HackerTarget API rate limit reached.[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 17. FORWARD IP LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

def forward_ip(domain: str):
    """Resolve a domain to its IP address."""
    domain = clean_domain(domain)
    ip     = get_ip_from_domain(domain)
    if ip:
        print_result(
            "Forward IP Lookup",
            f"[label]{domain}[/label]  [muted]→[/muted]  [primary]{ip}[/primary]",
        )
    else:
        console.print("[danger]Could not resolve domain to IP[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 18. REVERSE DNS LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

def reverse_dns(target: str):
    """PTR record lookup — IP → hostname."""
    target = clean_domain(target)
    ip     = target if is_ip(target) else get_ip_from_domain(target)
    if not ip:
        console.print("[danger]Cannot resolve host to IP[/danger]")
        return
    try:
        host = socket.gethostbyaddr(ip)[0]
        print_result(
            "Reverse DNS Lookup",
            f"[label]{ip}[/label]  [muted]→[/muted]  [primary]{host}[/primary]",
        )
    except Exception:
        print_result("Reverse DNS Lookup",
                     f"[warning]No PTR record found for {ip}[/warning]")
