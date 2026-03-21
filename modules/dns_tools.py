#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/dns_tools.py
DNS feature modules:
  8.  DNS Records (Full)
  9.  Domain WHOIS
  10. Subdomain Enumeration
  11. DNS Zone Transfer
  12. Shared DNS Lookup
  13. Forward DNS
"""

import socket
import threading
import concurrent.futures
from datetime import datetime

import requests
import dns.resolver
import dns.zone
import dns.query
import dns.rdatatype
import whois

from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich import box
from rich.table import Table

from modules.theme import console, BORDER_STYLE, PANEL_BORDER, TITLE_STYLE, MENU_OPT_STYLE
from modules.utils import clean_domain, print_result, section, spinner


# ============================================================
# 8 — DNS RECORDS (FULL ENUMERATION)
# ============================================================

def dns_records(domain: str) -> None:
    """Query all common DNS record types for a domain."""
    domain = clean_domain(domain)
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "SRV", "CAA"]
    info = ""

    with spinner(f"Enumerating DNS records for {domain}...") as p:
        p.add_task("dns")
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                info += section(f"{rtype} Records")
                for rdata in answers:
                    info += f"  [accent]◆[/accent] [value]{rdata}[/value]\n"
            except Exception:
                pass

    if info:
        print_result("DNS Records (Full)", info, subtitle=domain)
    else:
        console.print(f"[warning]No DNS records found for {domain}[/warning]")


# ============================================================
# 9 — DOMAIN WHOIS
# ============================================================

def domain_whois(domain: str) -> None:
    """Full WHOIS lookup with expiry countdown."""
    domain = clean_domain(domain)
    try:
        with spinner(f"Querying WHOIS for {domain}...") as p:
            p.add_task("w")
            w = whois.whois(domain)

        def fmt(val):
            if val is None:
                return "N/A"
            if isinstance(val, list):
                val = val[0]
            if isinstance(val, datetime):
                return val.strftime("%Y-%m-%d %H:%M:%S UTC")
            return str(val)

        # Expiry countdown
        exp = w.expiration_date
        if isinstance(exp, list):
            exp = exp[0]
        days_left = ""
        if isinstance(exp, datetime):
            delta = (exp - datetime.utcnow()).days
            if delta > 60:
                days_left = f"  [open]({delta} days left)[/open]"
            elif delta > 0:
                days_left = f"  [warning]({delta} days — EXPIRING SOON!)[/warning]"
            else:
                days_left = f"  [danger](EXPIRED {abs(delta)} days ago)[/danger]"

        info  = section("Registration")
        info += f"[label]Domain       :[/label] [value]{fmt(w.domain_name)}[/value]\n"
        info += f"[label]Registrar    :[/label] [value]{fmt(w.registrar)}[/value]\n"
        info += f"[label]Created      :[/label] [value]{fmt(w.creation_date)}[/value]\n"
        info += f"[label]Updated      :[/label] [value]{fmt(w.updated_date)}[/value]\n"
        info += f"[label]Expires      :[/label] [value]{fmt(w.expiration_date)}[/value]{days_left}\n"
        info += f"[label]Status       :[/label] [value]{fmt(w.status)}[/value]\n"

        info += section("Registrant")
        info += f"[label]Organization :[/label] [value]{fmt(w.org)}[/value]\n"
        info += f"[label]Country      :[/label] [value]{fmt(w.country)}[/value]\n"
        info += f"[label]State        :[/label] [value]{fmt(w.state)}[/value]\n"
        info += f"[label]Emails       :[/label] [value]{fmt(w.emails)}[/value]\n"

        info += section("Name Servers")
        ns = w.name_servers or []
        if isinstance(ns, str):
            ns = [ns]
        for n in sorted({str(x).lower() for x in ns}):
            info += f"  [accent]◆[/accent] [value]{n}[/value]\n"

        print_result("Domain WHOIS", info, subtitle=domain)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 10 — SUBDOMAIN ENUMERATION
# ============================================================

SUBDOMAIN_WORDLIST = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "ns1", "ns2", "ns3", "ns4",
    "vpn", "dev", "staging", "test", "api", "cdn", "blog", "shop", "portal",
    "admin", "dashboard", "login", "auth", "oauth", "secure", "static",
    "assets", "img", "images", "media", "video", "download", "files",
    "cloud", "app", "apps", "mobile", "m", "wap", "gateway", "proxy",
    "beta", "alpha", "demo", "sandbox", "lab", "labs", "internal",
    "intranet", "git", "gitlab", "bitbucket", "svn", "jira", "wiki", "docs",
    "status", "monitor", "metrics", "grafana", "jenkins", "ci", "build",
    "server", "web", "webmail", "cpanel", "whm", "autodiscover", "autoconfig",
    "remote", "ssh", "database", "db", "mysql", "postgres", "redis", "mongo",
    "backup", "old", "new", "v2", "v3", "v4", "help", "support", "kb", "forum",
    "community", "store", "pay", "billing", "invoice", "erp", "crm",
    "hub", "panel", "manage", "management", "control", "office", "corp",
    "smtp2", "smtp3", "mx1", "mx2", "relay", "bounce", "track",
    "search", "analytics", "stat", "stats", "report", "reports",
    "staging2", "uat", "qa", "preview", "preprod", "production",
]


def subdomain_enum(domain: str) -> None:
    """Brute-force subdomain enumeration using a built-in wordlist."""
    domain = clean_domain(domain)
    console.print(
        f"\n[primary]Enumerating subdomains of [accent]{domain}[/accent] "
        f"— {len(SUBDOMAIN_WORDLIST)} words, 40 threads...[/primary]\n"
    )

    found: list[tuple[str, str]] = []
    lock = threading.Lock()

    def check(sub: str) -> None:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            with lock:
                found.append((target, ip))
        except Exception:
            pass

    with Progress(
        SpinnerColumn(style="primary"),
        TextColumn("[primary]Checking subdomains...[/primary]"),
        BarColumn(bar_width=30, style="primary"),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("sub", total=len(SUBDOMAIN_WORDLIST))

        def worker(sub: str) -> None:
            check(sub)
            progress.update(task, advance=1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as ex:
            ex.map(worker, SUBDOMAIN_WORDLIST)

    found.sort(key=lambda x: x[0])

    if found:
        t = Table(
            show_header=True,
            box=box.SIMPLE_HEAD,
            border_style=BORDER_STYLE,
            header_style=MENU_OPT_STYLE,
        )
        t.add_column("Subdomain", style="accent")
        t.add_column("IP Address", style="value")

        for subdomain, ip in found:
            t.add_row(subdomain, ip)

        console.print(
            Panel(
                f"[open]✔  Found {len(found)} subdomain(s) for {domain}[/open]",
                title=f"[{TITLE_STYLE}]Subdomain Enumeration[/{TITLE_STYLE}]",
                border_style=PANEL_BORDER,
            )
        )
        console.print(t)
    else:
        print_result(
            "Subdomain Enumeration",
            f"[warning]No live subdomains found for {domain}[/warning]",
        )


# ============================================================
# 11 — DNS ZONE TRANSFER
# ============================================================

def zone_transfer(domain: str) -> None:
    """Attempt AXFR DNS zone transfer against all nameservers."""
    domain = clean_domain(domain)
    try:
        ns_records = dns.resolver.resolve(domain, "NS")
        attempted  = 0

        for ns in ns_records:
            ns_name = str(ns)
            try:
                ns_ip = dns.resolver.resolve(ns_name, "A")[0].to_text()
                console.print(f"[muted]  Trying AXFR: {ns_name} ({ns_ip})...[/muted]")
                attempted += 1
                zone = dns.zone.from_xfr(
                    dns.query.xfr(ns_ip, domain, timeout=10, lifetime=15)
                )
                if zone:
                    info  = f"[open]✔  Zone transfer SUCCESSFUL from {ns_name} ({ns_ip})[/open]\n\n"
                    for name, node in zone.nodes.items():
                        for rdataset in node.rdatasets:
                            rtype_str = dns.rdatatype.to_text(rdataset.rdtype)
                            for rdata in rdataset:
                                info += (
                                    f"  [accent]{name}[/accent]  "
                                    f"[muted]{rdataset.ttl}[/muted]  "
                                    f"[value]{rtype_str}  {rdata}[/value]\n"
                                )
                    print_result("DNS Zone Transfer", info, subtitle=domain)
                    return
            except Exception as e:
                console.print(f"[muted]    ✗ Failed: {e}[/muted]")
                continue

        print_result(
            "DNS Zone Transfer",
            f"[warning]Zone transfer blocked on all {attempted} nameserver(s).\n"
            f"This is expected — most modern DNS servers disable AXFR.[/warning]",
            subtitle=domain,
        )

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 12 — SHARED DNS LOOKUP
# ============================================================

def shared_dns(domain: str) -> None:
    """Find domains sharing the same nameserver via HackerTarget API."""
    domain = clean_domain(domain)
    try:
        with spinner(f"Finding shared DNS for {domain}...") as p:
            p.add_task("sharedns")
            r = requests.get(
                f"https://api.hackertarget.com/findshareddns/?q={domain}",
                timeout=15,
            )
        data = r.text.strip()
        if data and "error" not in data.lower() and "API count" not in data.lower():
            domains = [d.strip() for d in data.split("\n") if d.strip()]
            info = f"[open]Found {len(domains)} domain(s) sharing DNS with {domain}[/open]\n\n"
            for d in domains:
                info += f"  [accent]◆[/accent] [value]{d}[/value]\n"
            print_result("Shared DNS Lookup", info, subtitle=domain)
        else:
            console.print("[warning]No results — or HackerTarget free API limit reached.[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 13 — FORWARD DNS
# ============================================================

def forward_dns(domain: str) -> None:
    """Forward DNS lookup — all common record types."""
    domain = clean_domain(domain)
    try:
        info = ""
        for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                info += section(rtype)
                for rdata in answers:
                    info += f"  [accent]◆[/accent] [value]{rdata}[/value]\n"
            except Exception:
                pass

        if info:
            print_result("Forward DNS", info, subtitle=domain)
        else:
            console.print(f"[warning]No DNS records found for {domain}[/warning]")

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")
