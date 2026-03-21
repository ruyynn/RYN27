#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/dns_module.py
DNS features: full records, subdomain enum, zone transfer,
forward DNS, shared DNS lookup.
"""

import socket
import threading
import concurrent.futures

import requests
import dns.resolver
import dns.zone
import dns.query
import dns.rdatatype
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from modules.core import (
    console, clean_domain, print_result, section, spinner,
    TITLE_STYLE, PANEL_BORDER, BORDER_STYLE, MENU_OPT_STYLE
)


# ─────────────────────────────────────────────────────────────────────────────
# 8. DNS RECORDS — FULL ENUMERATION
# ─────────────────────────────────────────────────────────────────────────────

def dns_records(domain: str):
    """Enumerate A, AAAA, MX, NS, TXT, CNAME, SOA, SRV records."""
    domain = clean_domain(domain)
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "SRV"]
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
        print_result("DNS Records (Full)",
                     "[warning]No DNS records found — domain may not exist or DNS is down.[/warning]",
                     subtitle=domain)


# ─────────────────────────────────────────────────────────────────────────────
# 9. DOMAIN WHOIS
# ─────────────────────────────────────────────────────────────────────────────

def domain_whois(domain: str):
    """WHOIS lookup with expiry countdown."""
    import whois
    from datetime import datetime
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
        days_tag = ""
        if isinstance(exp, datetime):
            delta = (exp - datetime.utcnow()).days
            if delta > 60:
                days_tag = f"  [open]({delta} days left)[/open]"
            elif delta > 0:
                days_tag = f"  [warning]({delta} days — expiring soon!)[/warning]"
            else:
                days_tag = f"  [danger](EXPIRED {abs(delta)} days ago)[/danger]"

        info  = section("Registration")
        info += f"[label]Domain       :[/label] [value]{fmt(w.domain_name)}[/value]\n"
        info += f"[label]Registrar    :[/label] [value]{fmt(w.registrar)}[/value]\n"
        info += f"[label]Created      :[/label] [value]{fmt(w.creation_date)}[/value]\n"
        info += f"[label]Updated      :[/label] [value]{fmt(w.updated_date)}[/value]\n"
        info += f"[label]Expires      :[/label] [value]{fmt(w.expiration_date)}[/value]{days_tag}\n"
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
        for n in sorted(set(str(x).lower() for x in ns)):
            info += f"  [accent]◆[/accent] [value]{n}[/value]\n"

        print_result("Domain WHOIS", info, subtitle=domain)

    except Exception as e:
        console.print(f"[danger]WHOIS Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 10. SUBDOMAIN ENUMERATION
# ─────────────────────────────────────────────────────────────────────────────

SUBDOMAIN_WORDLIST = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "ns1", "ns2", "ns3", "ns4",
    "vpn", "dev", "staging", "test", "api", "cdn", "blog", "shop", "portal",
    "admin", "dashboard", "login", "auth", "oauth", "secure", "static",
    "assets", "img", "images", "media", "video", "download", "files",
    "cloud", "app", "apps", "mobile", "m", "wap", "gateway", "proxy",
    "beta", "alpha", "demo", "sandbox", "lab", "labs", "internal",
    "intranet", "git", "gitlab", "bitbucket", "svn", "jira", "wiki", "docs",
    "status", "monitor", "metrics", "grafana", "kibana", "jenkins", "ci", "build",
    "server", "web", "webmail", "cpanel", "whm", "autodiscover", "autoconfig",
    "remote", "ssh", "database", "db", "mysql", "postgres", "redis", "mongo",
    "backup", "old", "new", "v2", "v3", "v4", "help", "support", "kb", "forum",
    "community", "store", "pay", "billing", "invoice", "erp", "crm",
    "smtp2", "email", "mx", "relay", "exchange", "office", "owa",
    "management", "manager", "control", "panel", "cp", "admin2",
    "api2", "api3", "apidev", "devapi", "staging2", "preview",
]

def subdomain_enum(domain: str):
    """Threaded subdomain enumeration via DNS resolution."""
    domain = clean_domain(domain)
    console.print(
        f"\n[primary]Enumerating subdomains of [accent]{domain}[/accent] "
        f"({len(SUBDOMAIN_WORDLIST)} words)...[/primary]\n"
    )

    found = []
    lock  = threading.Lock()

    def check(sub: str):
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
        BarColumn(bar_width=35),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("sub", total=len(SUBDOMAIN_WORDLIST))

        def worker(sub: str):
            check(sub)
            progress.update(task, advance=1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
            ex.map(worker, SUBDOMAIN_WORDLIST)

    found.sort(key=lambda x: x[0])

    if found:
        t = Table(
            show_header=True, box=box.SIMPLE_HEAD,
            border_style=BORDER_STYLE, header_style=MENU_OPT_STYLE,
        )
        t.add_column("Subdomain", style="accent")
        t.add_column("IP Address", style="value")
        for sd, ip in found:
            t.add_row(sd, ip)

        console.print(Panel(
            f"[open]Found {len(found)} active subdomain(s)[/open]",
            title=f"[{TITLE_STYLE}]Subdomain Enumeration[/{TITLE_STYLE}]",
            border_style=PANEL_BORDER,
            padding=(0, 2),
        ))
        console.print(t)
    else:
        print_result("Subdomain Enumeration",
                     "[warning]No subdomains resolved — all DNS lookups returned NXDOMAIN.[/warning]",
                     subtitle=domain)


# ─────────────────────────────────────────────────────────────────────────────
# 11. DNS ZONE TRANSFER
# ─────────────────────────────────────────────────────────────────────────────

def zone_transfer(domain: str):
    """Attempt AXFR zone transfer against all authoritative nameservers."""
    domain = clean_domain(domain)
    try:
        ns_records = dns.resolver.resolve(domain, "NS")
        attempted  = 0
        for ns in ns_records:
            ns_name = str(ns)
            try:
                ns_ip = dns.resolver.resolve(ns_name, "A")[0].to_text()
                console.print(f"[muted]Trying AXFR from {ns_name} ({ns_ip})...[/muted]")
                attempted += 1
                zone = dns.zone.from_xfr(
                    dns.query.xfr(ns_ip, domain, timeout=10, lifetime=15)
                )
                if zone:
                    info = f"[open]Zone transfer SUCCESSFUL from {ns_name} ({ns_ip})[/open]\n\n"
                    for name, node in zone.nodes.items():
                        for rdataset in node.rdatasets:
                            for rdata in rdataset:
                                info += (
                                    f"  [accent]{name}[/accent]  [muted]{rdataset.ttl}[/muted]  "
                                    f"[value]{dns.rdatatype.to_text(rdataset.rdtype)}  {rdata}[/value]\n"
                                )
                    print_result("DNS Zone Transfer", info, subtitle=domain)
                    return
            except Exception as e:
                console.print(f"[muted]  ✘ {ns_name}: {e}[/muted]")
                continue

        print_result(
            "DNS Zone Transfer",
            f"[warning]AXFR blocked on all {attempted} nameserver(s).\n"
            f"[muted]This is normal — zone transfer is disabled on properly secured DNS servers.[/muted][/warning]",
            subtitle=domain,
        )
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 12. SHARED DNS LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

def shared_dns(domain: str):
    """Find domains sharing the same nameserver (via HackerTarget API)."""
    domain = clean_domain(domain)
    try:
        with spinner(f"Finding shared DNS for {domain}...") as p:
            p.add_task("sharedns")
            r = requests.get(
                f"https://api.hackertarget.com/findshareddns/?q={domain}", timeout=15
            )
        data = r.text.strip()
        if data and "error" not in data.lower() and "API count" not in data.lower():
            domains = [d.strip() for d in data.split("\n") if d.strip()]
            info    = f"[open]Found {len(domains)} domain(s) sharing DNS with {domain}[/open]\n\n"
            for d in domains:
                info += f"  [accent]◆[/accent] [value]{d}[/value]\n"
            print_result("Shared DNS Lookup", info, subtitle=domain)
        else:
            console.print("[warning]No results or HackerTarget API rate limit reached.[/warning]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 13. FORWARD DNS
# ─────────────────────────────────────────────────────────────────────────────

def forward_dns(domain: str):
    """Resolve A, AAAA, MX, NS, TXT, CNAME for a domain."""
    domain = clean_domain(domain)
    try:
        info = ""
        for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                info += section(rtype)
                for rdata in answers:
                    info += f"  [accent]◆[/accent] [value]{rdata}[/value]\n"
            except Exception:
                pass
        if info:
            print_result("Forward DNS Lookup", info, subtitle=domain)
        else:
            print_result("Forward DNS Lookup",
                         "[warning]No DNS records resolved for this domain.[/warning]",
                         subtitle=domain)
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")
