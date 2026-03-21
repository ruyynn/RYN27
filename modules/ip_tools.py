#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/ip_tools.py
IP and host feature modules:
  14. IP Geolocation
  15. Port Scan (Threaded)
  16. Reverse IP Lookup
  17. Forward IP Lookup
  18. Reverse DNS Lookup
  19. SSL/TLS Certificate Inspector
"""

import socket
import ssl
import threading
import concurrent.futures
from datetime import datetime

import requests
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich import box
from rich.table import Table

from modules.theme import (
    console, BORDER_STYLE, PANEL_BORDER, TITLE_STYLE, MENU_OPT_STYLE,
)
from modules.utils import (
    clean_domain, is_ip, get_ip_from_domain,
    print_result, section, spinner,
)


# ============================================================
# 14 — IP GEOLOCATION
# ============================================================

def ip_location(target: str) -> None:
    """Geolocate an IP or domain via ip-api.com (free tier)."""
    target = clean_domain(target)
    try:
        ip = target if is_ip(target) else socket.gethostbyname(target)

        with spinner(f"Geolocating {ip}...") as p:
            p.add_task("geo")
            r = requests.get(
                f"http://ip-api.com/json/{ip}"
                f"?fields=status,message,country,countryCode,regionName,city,"
                f"zip,lat,lon,isp,org,as,asname,mobile,proxy,hosting,query",
                timeout=10,
            )
        data = r.json()
        if data.get("status") != "success":
            console.print(f"[danger]Error: {data.get('message','Unknown error')}[/danger]")
            return

        # Flag emoji
        cc   = data.get("countryCode", "")
        flag = "".join(chr(0x1F1E0 + ord(c) - ord("A")) for c in cc) if len(cc) == 2 else ""

        info  = section("Location")
        info += f"[label]IP Address   :[/label] [primary]{data['query']}[/primary]\n"
        info += f"[label]Country      :[/label] [value]{flag} {data['country']} ({cc})[/value]\n"
        info += f"[label]Region       :[/label] [value]{data['regionName']}[/value]\n"
        info += f"[label]City         :[/label] [value]{data['city']}[/value]\n"
        info += f"[label]ZIP          :[/label] [value]{data.get('zip','N/A')}[/value]\n"
        info += f"[label]Coordinates  :[/label] [accent]{data['lat']}, {data['lon']}[/accent]\n"
        info += (
            f"[label]Maps Link    :[/label] "
            f"[muted]https://maps.google.com/?q={data['lat']},{data['lon']}[/muted]\n"
        )

        info += section("Network")
        info += f"[label]ISP          :[/label] [value]{data['isp']}[/value]\n"
        info += f"[label]Organization :[/label] [value]{data['org']}[/value]\n"
        info += f"[label]AS Number    :[/label] [value]{data['as']}[/value]\n"
        info += f"[label]AS Name      :[/label] [value]{data.get('asname','N/A')}[/value]\n"

        info += section("Flags")
        mobile_s  = "[open]YES[/open]"   if data.get("mobile")  else "[closed]NO[/closed]"
        proxy_s   = "[danger]YES — PROXY/VPN DETECTED[/danger]" if data.get("proxy")   else "[open]NO[/open]"
        hosting_s = "[warning]YES[/warning]"                     if data.get("hosting") else "[open]NO[/open]"
        info += f"[label]Mobile       :[/label] {mobile_s}\n"
        info += f"[label]Proxy / VPN  :[/label] {proxy_s}\n"
        info += f"[label]Hosting / DC :[/label] {hosting_s}\n"

        print_result("IP Geolocation", info, subtitle=ip)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 15 — PORT SCAN (THREADED + BANNER GRAB)
# ============================================================

COMMON_PORTS: dict[int, str] = {
    21:    "FTP",
    22:    "SSH",
    23:    "Telnet",
    25:    "SMTP",
    53:    "DNS",
    80:    "HTTP",
    110:   "POP3",
    111:   "RPC",
    135:   "MSRPC",
    139:   "NetBIOS",
    143:   "IMAP",
    443:   "HTTPS",
    445:   "SMB",
    465:   "SMTPS",
    587:   "SMTP-TLS",
    993:   "IMAPS",
    995:   "POP3S",
    1433:  "MSSQL",
    1723:  "PPTP",
    3306:  "MySQL",
    3389:  "RDP",
    5432:  "PostgreSQL",
    5900:  "VNC",
    6379:  "Redis",
    8080:  "HTTP-ALT",
    8443:  "HTTPS-ALT",
    8888:  "HTTP-DEV",
    27017: "MongoDB",
}


def _scan_port(host: str, port: int, timeout: float = 1.2) -> tuple[bool, str]:
    """Attempt TCP connect to host:port; try banner grab on success."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) != 0:
            sock.close()
            return False, ""
        # Banner grab
        banner = ""
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
        return True, banner
    except Exception:
        return False, ""


def port_scan(host: str) -> None:
    """Threaded TCP port scan with banner grabbing across 28 common ports."""
    host = clean_domain(host)
    if not is_ip(host):
        ip = get_ip_from_domain(host)
        if not ip:
            console.print("[danger]Cannot resolve host[/danger]")
            return
        host = ip

    console.print(
        f"\n[primary]Scanning [accent]{host}[/accent] "
        f"— {len(COMMON_PORTS)} ports, 30 threads...[/primary]\n"
    )

    open_ports: list[tuple[int, str, str]] = []
    lock = threading.Lock()

    with Progress(
        SpinnerColumn(style="primary"),
        TextColumn("[primary]Scanning port {task.fields[port]}[/primary]"),
        BarColumn(bar_width=30, style="primary"),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("scan", total=len(COMMON_PORTS), port="...")

        def check(port: int) -> None:
            progress.update(task, advance=1, port=str(port))
            ok, banner = _scan_port(host, port)
            if ok:
                with lock:
                    open_ports.append((port, COMMON_PORTS.get(port, "unknown"), banner))

        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            ex.map(check, COMMON_PORTS.keys())

    open_ports.sort(key=lambda x: x[0])

    if open_ports:
        t = Table(
            show_header=True,
            box=box.SIMPLE_HEAD,
            border_style=BORDER_STYLE,
            header_style=MENU_OPT_STYLE,
        )
        t.add_column("Port",    style="accent", width=8)
        t.add_column("Service", style="value",  width=14)
        t.add_column("State",   style="open",   width=8)
        t.add_column("Banner",  style="muted")

        for port, service, banner in open_ports:
            t.add_row(str(port), service, "OPEN", banner or "—")

        from rich.panel import Panel
        console.print(
            Panel(
                f"[open]✔  Found {len(open_ports)} open port(s) on {host}[/open]",
                title=f"[{TITLE_STYLE}]Port Scan[/{TITLE_STYLE}]",
                border_style=PANEL_BORDER,
            )
        )
        console.print(t)
    else:
        print_result(
            "Port Scan",
            f"[warning]No open ports found on {host} (scanned {len(COMMON_PORTS)} ports)[/warning]",
        )


# ============================================================
# 16 — REVERSE IP LOOKUP
# ============================================================

def reverse_ip(target: str) -> None:
    """Find all domains hosted on the same IP via HackerTarget API."""
    target = clean_domain(target)
    ip = target if is_ip(target) else get_ip_from_domain(target)
    if not ip:
        console.print("[danger]Cannot resolve host[/danger]")
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
            console.print("[warning]No results — or HackerTarget free API limit reached.[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 17 — FORWARD IP LOOKUP
# ============================================================

def forward_ip(domain: str) -> None:
    """Resolve a domain to its IPv4 address."""
    domain = clean_domain(domain)
    ip = get_ip_from_domain(domain)
    if ip:
        print_result("Forward IP", f"[label]{domain}[/label] [muted]→[/muted] [primary]{ip}[/primary]")
    else:
        console.print(f"[danger]Could not resolve: {domain}[/danger]")


# ============================================================
# 18 — REVERSE DNS LOOKUP
# ============================================================

def reverse_dns(target: str) -> None:
    """PTR record lookup — IP to hostname."""
    target = clean_domain(target)
    ip     = target if is_ip(target) else get_ip_from_domain(target)
    if not ip:
        console.print("[danger]Cannot resolve host[/danger]")
        return
    try:
        host = socket.gethostbyaddr(ip)[0]
        print_result("Reverse DNS", f"[label]{ip}[/label] [muted]→[/muted] [primary]{host}[/primary]")
    except Exception:
        console.print(f"[danger]No PTR record found for {ip}[/danger]")


# ============================================================
# 19 — SSL/TLS CERTIFICATE INSPECTOR
# ============================================================

def ssl_info(target: str) -> None:
    """Inspect SSL/TLS certificate — expiry, issuer, SAN, cipher."""
    domain = clean_domain(target)
    try:
        with spinner(f"Fetching SSL/TLS cert for {domain}...") as p:
            p.add_task("ssl")
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
                socket.create_connection((domain, 443), timeout=10),
                server_hostname=domain,
            ) as ssock:
                cert     = ssock.getpeercert()
                protocol = ssock.version()
                cipher   = ssock.cipher()

        subject    = dict(x[0] for x in cert.get("subject", []))
        issuer     = dict(x[0] for x in cert.get("issuer",  []))
        not_before = cert.get("notBefore", "N/A")
        not_after  = cert.get("notAfter",  "N/A")
        san        = cert.get("subjectAltName", [])

        # Expiry check
        try:
            exp_dt    = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            days_left = (exp_dt - datetime.utcnow()).days
            if days_left > 30:
                exp_str = f"[open]{not_after} ({days_left}d remaining)[/open]"
            elif days_left > 0:
                exp_str = f"[warning]{not_after} ({days_left}d — EXPIRING SOON!)[/warning]"
            else:
                exp_str = f"[danger]{not_after} — EXPIRED[/danger]"
        except Exception:
            exp_str = not_after

        info  = section("Certificate Details")
        info += f"[label]Common Name  :[/label] [value]{subject.get('commonName','N/A')}[/value]\n"
        info += f"[label]Organization :[/label] [value]{subject.get('organizationName','N/A')}[/value]\n"
        info += f"[label]Valid From   :[/label] [value]{not_before}[/value]\n"
        info += f"[label]Valid Until  :[/label] {exp_str}\n"
        info += f"[label]Serial No.   :[/label] [muted]{cert.get('serialNumber','N/A')}[/muted]\n"

        info += section("Issuer")
        info += f"[label]Issuer CN    :[/label] [value]{issuer.get('commonName','N/A')}[/value]\n"
        info += f"[label]Issuer Org   :[/label] [value]{issuer.get('organizationName','N/A')}[/value]\n"

        info += section("TLS Connection")
        info += f"[label]Protocol     :[/label] [accent]{protocol}[/accent]\n"
        info += f"[label]Cipher Suite :[/label] [value]{cipher[0] if cipher else 'N/A'}[/value]\n"
        info += f"[label]Key Bits     :[/label] [value]{cipher[2] if cipher else 'N/A'}[/value]\n"

        if san:
            info += section(f"Subject Alt Names ({len(san)})")
            for _, name in san[:25]:
                info += f"  [accent]◆[/accent] [value]{name}[/value]\n"
            if len(san) > 25:
                info += f"  [muted]... and {len(san)-25} more[/muted]\n"

        print_result("SSL/TLS Certificate", info, subtitle=domain)

    except ssl.SSLError as e:
        console.print(f"[danger]SSL Error: {e}[/danger]")
    except ConnectionRefusedError:
        console.print(f"[danger]Port 443 is closed on {domain}[/danger]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")
