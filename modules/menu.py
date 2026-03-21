#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/menu.py
Main menu, tutorial/usage guide, about page, and star CTA.
"""

from rich.panel  import Panel
from rich.table  import Table
from rich.text   import Text
from rich.rule   import Rule
from rich.align  import Align
from rich.columns import Columns
from rich        import box

from modules.theme import (
    console,
    BORDER_STYLE, PANEL_BORDER, TITLE_STYLE,
    MENU_OPT_STYLE, MENU_FN_STYLE, MENU_CAT_STYLE,
    PROMPT_STYLE,
)
from modules.logo  import NEW_LOGO
from modules.utils import VERSION, AUTHOR, GITHUB_URL, GITHUB_USER

# ============================================================
# MENU DEFINITION
# ============================================================

MENU_CATEGORIES = [
    # (option_str, label, input_hint)   — None label = section header
    ("── WEB RECON ──",       None,  None),
    ("[1]",  "Website Information",       "URL / Domain"),
    ("[2]",  "HTTP Security Audit",       "URL / Domain"),
    ("[3]",  "Technology Detection",      "URL / Domain"),
    ("[4]",  "Metadata Crawler",          "URL / Domain"),
    ("[5]",  "Robots.txt & Sitemap",      "URL / Domain"),
    ("[6]",  "Email / Contact Harvest",   "URL / Domain"),
    ("[7]",  "Full Website Recon",        "URL / Domain"),
    ("── DNS / NETWORK ──",   None,  None),
    ("[8]",  "DNS Records (Full)",        "Domain"),
    ("[9]",  "Domain WHOIS",              "Domain"),
    ("[10]", "Subdomain Enumeration",     "Domain"),
    ("[11]", "DNS Zone Transfer",         "Domain"),
    ("[12]", "Shared DNS Lookup",         "Domain"),
    ("[13]", "Forward DNS",               "Domain"),
    ("── IP / HOST ──",       None,  None),
    ("[14]", "IP Geolocation",            "IP / Domain"),
    ("[15]", "Port Scan (Threaded)",      "IP / Domain"),
    ("[16]", "Reverse IP Lookup",         "IP / Domain"),
    ("[17]", "Forward IP Lookup",         "Domain"),
    ("[18]", "Reverse DNS Lookup",        "IP / Domain"),
    ("── SSL ──",             None,  None),
    ("[19]", "SSL/TLS Certificate",       "Domain"),
    ("── EXTRAS ──",          None,  None),
    ("[20]", "Tutorial / Usage Guide",    ""),
    ("[21]", "About RYN27",               ""),
    ("[22]", "⭐ Give a Star",            ""),
    ("──────────────────",    None,  None),
    ("[0]",  "Exit",                      ""),
]


def create_premium_menu() -> Table:
    t = Table(
        show_header=False,
        box=box.SIMPLE,
        border_style=BORDER_STYLE,
        pad_edge=False,
        show_edge=False,
    )
    t.add_column("Opt",  style=MENU_OPT_STYLE, width=6)
    t.add_column("Func", style=MENU_FN_STYLE,  width=30)
    t.add_column("In",   style="muted",         width=12)

    for item in MENU_CATEGORIES:
        opt, func, inp = item
        if func is None:
            t.add_row("", f"[{MENU_CAT_STYLE}]{opt}[/{MENU_CAT_STYLE}]", "")
        else:
            t.add_row(opt, func, inp or "")
    return t


def show_menu() -> None:
    """Render the main interactive menu panel."""
    menu_table = create_premium_menu()
    logo_text  = Text(NEW_LOGO, style="star")
    columns    = Columns([menu_table, logo_text], equal=False, expand=True)

    subtitle = (
        f"[muted]v{VERSION}  •  by @{AUTHOR}  •  "
        f"bug bounty | CTF | pentesting | education[/muted]"
    )

    console.print(
        Panel(
            columns,
            title=f"[{TITLE_STYLE}]⚡  RYN27 RECON TOOL  ⚡[/{TITLE_STYLE}]",
            subtitle=subtitle,
            border_style=PANEL_BORDER,
            title_align="center",
            subtitle_align="center",
            padding=(1, 2),
        )
    )


# ============================================================
# TUTORIAL / USAGE GUIDE
# ============================================================

def show_tutorial() -> None:
    """Display a comprehensive usage guide inside the terminal."""
    console.print()
    console.print(Rule(f"[{TITLE_STYLE}]◈  RYN27 Tutorial & Usage Guide  ◈[/{TITLE_STYLE}]", style=BORDER_STYLE))
    console.print()

    # ── Installation ──────────────────────────────────────────
    inst = (
        "[label]Linux / macOS[/label]\n"
        "  [accent]git clone https://github.com/ruyynn/RYN27.git[/accent]\n"
        "  [accent]cd RYN27[/accent]\n"
        "  [accent]python3 RYN27.py[/accent]\n\n"
        "[label]Windows[/label]\n"
        "  [accent]git clone https://github.com/ruyynn/RYN27.git[/accent]\n"
        "  [accent]cd RYN27[/accent]\n"
        "  [accent]python RYN27.py[/accent]\n\n"
        "[label]Termux (Android)[/label]\n"
        "  [accent]pkg update && pkg upgrade[/accent]\n"
        "  [accent]pkg install python git[/accent]\n"
        "  [accent]git clone https://github.com/ruyynn/RYN27.git[/accent]\n"
        "  [accent]cd RYN27 && python RYN27.py[/accent]\n\n"
        "[label]Manual pip install (if auto-install fails)[/label]\n"
        "  [accent]pip install requests rich python-whois dnspython[/accent]\n"
        "  [accent]       builtwith beautifulsoup4 cryptography[/accent]"
    )
    console.print(
        Panel(inst, title=f"[{TITLE_STYLE}]📦 Installation[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()

    # ── Feature Guide table ───────────────────────────────────
    guide: list[tuple[str, str, str, str]] = [
        # (opt, name, accepts, description)
        ("1",  "Website Information",   "URL/Domain",
         "Fetches status code, response time, server header, page title, cookies,\n"
         "      redirect chain, and a quick security-header summary."),
        ("2",  "HTTP Security Audit",   "URL/Domain",
         "Checks 10 critical HTTP security headers (HSTS, CSP, X-Frame, etc.)\n"
         "      and returns a 0–100% security score."),
        ("3",  "Technology Detection",  "URL/Domain",
         "Identifies the tech stack (CMS, framework, CDN, analytics)\n"
         "      via builtwith + header fingerprinting."),
        ("4",  "Metadata Crawler",      "URL/Domain",
         "Extracts all <meta> tags, Open Graph (og:), Twitter Card,\n"
         "      <link> tags, and external script URLs."),
        ("5",  "Robots & Sitemap",      "URL/Domain",
         "Reads /robots.txt, /sitemap.xml, /sitemap_index.xml\n"
         "      and displays their contents in parsed form."),
        ("6",  "Email/Contact Harvest", "URL/Domain",
         "Regex-extracts email addresses, phone numbers, and\n"
         "      social media links (FB, IG, LinkedIn, GitHub, TG…)"),
        ("7",  "Full Website Recon",    "URL/Domain",
         "Combo: Website Info + HTTP Security Audit + Tech Detection\n"
         "      in a single pass — ideal for quick initial recon."),
        ("8",  "DNS Records (Full)",    "Domain",
         "Queries A, AAAA, MX, NS, TXT, CNAME, SOA, SRV, CAA records\n"
         "      — full picture of a domain's DNS configuration."),
        ("9",  "Domain WHOIS",          "Domain",
         "Full WHOIS lookup: registrar, creation/expiry date with\n"
         "      countdown, registrant org/country, name servers."),
        ("10", "Subdomain Enum",        "Domain",
         "DNS brute-force using a ~100-word built-in wordlist\n"
         "      with 40 concurrent threads. Fast and dependency-free."),
        ("11", "DNS Zone Transfer",     "Domain",
         "Attempts AXFR against all nameservers. Succeeds only\n"
         "      on misconfigured DNS servers — educational use."),
        ("12", "Shared DNS Lookup",     "Domain",
         "Finds domains sharing the same nameserver via\n"
         "      HackerTarget's free API."),
        ("13", "Forward DNS",           "Domain",
         "Forward DNS lookup for A, AAAA, MX, NS, TXT, CNAME, SOA."),
        ("14", "IP Geolocation",        "IP/Domain",
         "Geolocates an IP: country (with emoji flag), region, city,\n"
         "      ISP, AS number, proxy/VPN detection, Google Maps link."),
        ("15", "Port Scan",             "IP/Domain",
         "Threaded TCP port scan across 28 common ports (30 workers).\n"
         "      Includes service name and HTTP banner grabbing."),
        ("16", "Reverse IP",            "IP/Domain",
         "Finds all domains hosted on the same IP address\n"
         "      via HackerTarget reverseiplookup API."),
        ("17", "Forward IP",            "Domain",
         "Resolves a domain name to its IPv4 address (A record)."),
        ("18", "Reverse DNS",           "IP/Domain",
         "PTR record lookup — resolves an IP back to its hostname."),
        ("19", "SSL/TLS Certificate",   "Domain",
         "Inspects the SSL/TLS certificate: validity dates with\n"
         "      expiry countdown, issuer, SAN list, cipher suite."),
    ]

    t = Table(
        show_header=True,
        box=box.SIMPLE_HEAD,
        border_style=BORDER_STYLE,
        header_style=MENU_OPT_STYLE,
        padding=(0, 1),
    )
    t.add_column("#",       style="accent",    width=4,  no_wrap=True)
    t.add_column("Feature", style="label",     width=22, no_wrap=True)
    t.add_column("Input",   style="muted",     width=12, no_wrap=True)
    t.add_column("What it does", style="value")

    for opt, name, inp, desc in guide:
        t.add_row(opt, name, inp, desc)

    console.print(
        Panel(t, title=f"[{TITLE_STYLE}]📖 Feature Reference[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 1))
    )
    console.print()

    # ── Tips ──────────────────────────────────────────────────
    tips = (
        "[accent]◆[/accent] [label]Input formats accepted:[/label]\n"
        "    Domain  →  [value]example.com[/value]  or  [value]www.example.com[/value]\n"
        "    URL     →  [value]https://example.com/page[/value]  (protocol is stripped/normalized automatically)\n"
        "    IP      →  [value]8.8.8.8[/value]  (IPv4 only)\n\n"
        "[accent]◆[/accent] [label]For subdomain enumeration (option 10):[/label]\n"
        "    Enter the [value]root domain[/value] without www, e.g.  [value]example.com[/value]\n\n"
        "[accent]◆[/accent] [label]For SSL inspection (option 19):[/label]\n"
        "    Enter just the [value]domain[/value] — no https://  e.g.  [value]example.com[/value]\n\n"
        "[accent]◆[/accent] [label]HackerTarget API (options 12 & 16):[/label]\n"
        "    Free tier has a rate limit. If you hit it, wait a few minutes.\n\n"
        "[accent]◆[/accent] [label]Port scan speed:[/label]\n"
        "    30 threads with 1.2 s timeout. For distant hosts, results may\n"
        "    vary. The tool does not support stealth/SYN scans.\n\n"
        "[accent]◆[/accent] [label]Legal reminder:[/label]\n"
        "    [warning]Only run this tool against targets you own or have written\n"
        "    permission to test. Unauthorized scanning is illegal.[/warning]"
    )
    console.print(
        Panel(tips, title=f"[{TITLE_STYLE}]💡 Tips & Best Practices[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()

    # ── Quick examples ────────────────────────────────────────
    examples = (
        "[label]Recon a website quickly:[/label]\n"
        "  Choose [accent][7][/accent]  →  enter [value]example.com[/value]\n\n"
        "[label]Check if a domain is about to expire:[/label]\n"
        "  Choose [accent][9][/accent]  →  enter [value]example.com[/value]  →  look at Expires field\n\n"
        "[label]Find hidden subdomains:[/label]\n"
        "  Choose [accent][10][/accent] →  enter [value]example.com[/value]\n\n"
        "[label]Check SSL cert before it expires:[/label]\n"
        "  Choose [accent][19][/accent] →  enter [value]example.com[/value]\n\n"
        "[label]See what's running on a VPS:[/label]\n"
        "  Choose [accent][15][/accent] →  enter [value]your-server-ip[/value]\n\n"
        "[label]Investigate an IP address:[/label]\n"
        "  Choose [accent][14][/accent] →  enter [value]1.2.3.4[/value]  (geolocation + ISP + VPN check)\n"
        "  Choose [accent][16][/accent] →  same IP  (who else is on the same server?)\n"
        "  Choose [accent][18][/accent] →  same IP  (PTR / hostname)\n\n"
        "[label]Bug bounty recon workflow:[/label]\n"
        "  [accent][9][/accent] WHOIS  →  [accent][8][/accent] DNS Records  →  [accent][10][/accent] Subdomains  →  [accent][7][/accent] Full Recon  →  [accent][19][/accent] SSL"
    )
    console.print(
        Panel(examples, title=f"[{TITLE_STYLE}]⚡ Quick Examples[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()


# ============================================================
# ABOUT PAGE
# ============================================================

def show_about() -> None:
    """Display tool information, credits, and disclaimer."""
    console.print()
    console.print(Rule(f"[{TITLE_STYLE}]◈  About RYN27  ◈[/{TITLE_STYLE}]", style=BORDER_STYLE))
    console.print()

    about_text = (
        f"[label]Tool Name   :[/label]  [primary]RYN27[/primary] — Ultimate Information Gathering Tool\n"
        f"[label]Version     :[/label]  [accent]{VERSION}[/accent]\n"
        f"[label]Author      :[/label]  [secondary]{AUTHOR}[/secondary] 🇮🇩\n"
        f"[label]Repository  :[/label]  [link]{GITHUB_URL}[/link]\n"
        f"[label]License     :[/label]  [value]MIT — open source, free forever[/value]\n"
        f"[label]Platform    :[/label]  [value]Linux · macOS · Windows · Termux (Android)[/value]\n"
        f"[label]Language    :[/label]  [value]Python 3.9+[/value]\n"
    )
    console.print(
        Panel(about_text, title=f"[{TITLE_STYLE}]🔧 Tool Info[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()

    desc_text = (
        "[value]RYN27 is a CLI-based OSINT and information-gathering tool that combines[/value]\n"
        "[value]WHOIS, DNS enumeration, port scanning, IP geolocation, SSL inspection,[/value]\n"
        "[value]technology detection, and web recon into a single clean terminal interface.[/value]\n\n"
        "[value]Built for security researchers, bug bounty hunters, CTF players, and[/value]\n"
        "[value]sysadmins who need a fast, lightweight, no-nonsense recon tool that[/value]\n"
        "[value]runs anywhere Python does — including Android via Termux.[/value]"
    )
    console.print(
        Panel(desc_text, title=f"[{TITLE_STYLE}]📋 Description[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()

    # Dependencies table
    deps = Table(show_header=True, box=box.SIMPLE_HEAD, border_style=BORDER_STYLE,
                 header_style=MENU_OPT_STYLE)
    deps.add_column("Package",     style="accent", width=20)
    deps.add_column("Purpose",     style="value")
    deps.add_column("Auto-install", style="open",  width=14)
    for pkg, purpose in [
        ("requests",       "HTTP client for all web requests"),
        ("rich",           "Premium terminal UI — colors, panels, tables, progress bars"),
        ("python-whois",   "WHOIS domain lookups"),
        ("dnspython",      "Full DNS record enumeration & zone transfer"),
        ("builtwith",      "Technology stack fingerprinting"),
        ("beautifulsoup4", "HTML parsing for metadata & email extraction"),
        ("cryptography",   "SSL/TLS certificate parsing support"),
    ]:
        deps.add_row(pkg, purpose, "✔  YES")

    console.print(
        Panel(deps, title=f"[{TITLE_STYLE}]📦 Dependencies[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 1))
    )
    console.print()

    # Changelog
    changelog = (
        "[accent]v1.8.0[/accent]  [value]Modular architecture, 19 features, subdomain enum, SSL inspector,[/value]\n"
        "        [value]HTTP security audit, email harvester, robots/sitemap reader,[/value]\n"
        "        [value]threaded port scan with banner grab, tutorial & about pages.[/value]\n\n"
        "[accent]v1.0.0[/accent]  [value]Initial release — WHOIS, DNS, IP geo, port scan, tech detect,[/value]\n"
        "        [value]reverse/forward IP & DNS, zone transfer, metadata crawler.[/value]"
    )
    console.print(
        Panel(changelog, title=f"[{TITLE_STYLE}]📜 Changelog[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()

    # Disclaimer
    disclaimer = (
        "[warning]RYN27 is built ONLY for educational purposes and LEGAL security testing.[/warning]\n\n"
        "[open]✔  ALLOWED on:[/open]\n"
        "   [value]• Your own servers / websites[/value]\n"
        "   [value]• Targets with explicit written permission from the owner[/value]\n"
        "   [value]• Lab environments, CTF challenges, and official bug bounty platforms[/value]\n\n"
        "[danger]✘  PROHIBITED on:[/danger]\n"
        "   [value]• Other people's websites / servers without permission[/value]\n"
        "   [value]• Government and military infrastructure[/value]\n"
        "   [value]• Public or commercial services without consent[/value]\n\n"
        "[muted]The user is solely responsible for how this tool is used.\n"
        "The developer holds no liability for any misuse or damage caused.\n"
        "Violations may result in legal consequences under applicable cybercrime laws.[/muted]"
    )
    console.print(
        Panel(disclaimer, title=f"[{TITLE_STYLE}]⚠  Disclaimer[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()

    # Contact
    contact = (
        "[label]GitHub   :[/label]  [link]https://github.com/ruyynn[/link]\n"
        "[label]Facebook :[/label]  [link]https://web.facebook.com/profile.php?id=61587795784907[/link]\n"
        "[label]Email    :[/label]  [link]ruyynn25@gmail.com[/link]\n"
        "[label]Ko-fi    :[/label]  [link]https://ko-fi.com/H2H11W13IP[/link]\n"
        "[label]Saweria  :[/label]  [link]https://saweria.co/Ruyynn[/link]\n\n"
        "[muted]Got questions, collaboration offers, or bug reports?\n"
        "Feel free to open an issue or reach out directly.[/muted]"
    )
    console.print(
        Panel(contact, title=f"[{TITLE_STYLE}]📬 Contact & Support[/{TITLE_STYLE}]",
              border_style=PANEL_BORDER, padding=(1, 2))
    )
    console.print()


# ============================================================
# ⭐ STAR CTA
# ============================================================

def show_star_cta() -> None:
    """Display a full-screen star call-to-action panel."""
    console.print()
    console.print(Rule(style=BORDER_STYLE))
    console.print()

    cta_art = r"""
         *          *       *         *
      *     *    *     *       *   *
        *      ★   ★   ★   ★   ★      *
      *    ★                       ★    *
          ★    give this tool a ⭐    ★
      *    ★     it means a lot!    ★    *
        *      ★   ★   ★   ★   ★      *
      *     *    *     *       *   *
         *          *       *         *
    """
    console.print(Align.center(Text(cta_art, style="star")))
    console.print()

    body = (
        "[cta]If RYN27 has ever helped your work, learning, or bug bounty journey —[/cta]\n"
        "[cta]a ⭐ star on GitHub is the best way to say thank you![/cta]\n\n"
        "[value]It takes 2 seconds and it helps the tool get discovered by more people.[/value]\n"
        "[value]Every star motivates me to add more features and keep this free. 🙏[/value]\n\n"
        f"[label]👉  Star the repo here:[/label]\n"
        f"    [link]{GITHUB_URL}[/link]\n\n"
        "[muted]You can also support development by buying a coffee:[/muted]\n"
        "[link]    https://ko-fi.com/H2H11W13IP[/link]\n"
        "[link]    https://saweria.co/Ruyynn[/link]\n\n"
        "[muted]Coded with ❤️  by Ruyynn — from Indonesia 🇮🇩 for the global cybersecurity community[/muted]"
    )
    console.print(
        Panel(
            Align.center(body),
            title=f"[{TITLE_STYLE}]⭐  Support RYN27 — Give a Star!  ⭐[/{TITLE_STYLE}]",
            border_style=PANEL_BORDER,
            padding=(1, 4),
        )
    )
    console.print()
    console.print(Rule(style=BORDER_STYLE))
    console.print()
