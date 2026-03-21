#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/web_recon.py
Web recon features:
  1. Website Information
  2. HTTP Security Audit
  3. Technology Detection
  4. Metadata Crawler
  5. Robots.txt & Sitemap
  6. Email / Contact Harvester
  7. Full Website Recon (combo)
"""

import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from rich.rule import Rule

from modules.theme import (
    console, BORDER_STYLE, TITLE_STYLE,
)
from modules.utils import (
    ensure_url, clean_domain, print_result, section, spinner,
)

# ---- shared request headers ----
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
HEADERS = {"User-Agent": UA}


# ============================================================
# 1 — WEBSITE INFORMATION
# ============================================================

def website_info(url: str) -> None:
    """Fetch HTTP headers, status, title, cookies, redirect chain, security headers."""
    url = ensure_url(url)
    try:
        with spinner("Fetching website info...") as p:
            p.add_task("fetch")
            start   = time.time()
            session = requests.Session()
            r       = session.get(url, timeout=15, allow_redirects=True, headers=HEADERS)
            elapsed = time.time() - start

        soup     = BeautifulSoup(r.text, "html.parser")
        title_t  = soup.find("title")
        desc_t   = soup.find("meta", attrs={"name": "description"})
        gen_t    = soup.find("meta", attrs={"name": "generator"})

        sc = r.status_code
        if   sc < 300: sc_str = f"[open]{sc} OK[/open]"
        elif sc < 400: sc_str = f"[warning]{sc} REDIRECT[/warning]"
        else:          sc_str = f"[danger]{sc} ERROR[/danger]"

        info  = section("General")
        info += f"[label]URL           :[/label] [value]{r.url}[/value]\n"
        info += f"[label]Status Code   :[/label] {sc_str}\n"
        info += f"[label]Response Time :[/label] [accent]{elapsed:.3f}s[/accent]\n"
        info += f"[label]Title         :[/label] [value]{title_t.text.strip() if title_t else 'N/A'}[/value]\n"
        info += f"[label]Description   :[/label] [value]{desc_t['content'][:120] if desc_t and desc_t.get('content') else 'N/A'}[/value]\n"
        info += f"[label]Generator     :[/label] [value]{gen_t['content'] if gen_t and gen_t.get('content') else 'N/A'}[/value]\n"
        info += f"[label]Content-Type  :[/label] [value]{r.headers.get('Content-Type','N/A')}[/value]\n"
        info += f"[label]Server        :[/label] [value]{r.headers.get('Server','N/A')}[/value]\n"
        info += f"[label]Cookies       :[/label] [accent]{len(r.cookies)} found[/accent]\n"
        info += f"[label]Content-Len   :[/label] [value]{len(r.content):,} bytes[/value]\n"

        if r.history:
            info += section("Redirect Chain")
            for redir in r.history:
                info += f"  [muted]→[/muted] [warning]{redir.status_code}[/warning] [value]{redir.url}[/value]\n"
            info += f"  [muted]→[/muted] [open]{r.status_code}[/open] [value]{r.url}[/value]\n"

        sec_headers = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy":   "CSP",
            "X-Frame-Options":           "X-Frame-Options",
            "X-Content-Type-Options":    "X-Content-Type-Options",
            "Referrer-Policy":           "Referrer-Policy",
            "Permissions-Policy":        "Permissions-Policy",
        }
        info += section("Security Headers (quick)")
        for hdr, label in sec_headers.items():
            val = r.headers.get(hdr)
            if val:
                info += f"  [open]✔[/open] [accent]{label}[/accent]: [muted]{val[:60]}[/muted]\n"
            else:
                info += f"  [closed]✘[/closed] [muted]{label}: missing[/muted]\n"

        info += section("All HTTP Headers")
        for h, v in r.headers.items():
            info += f"  [accent]{h}:[/accent] [value]{v}[/value]\n"

        if r.cookies:
            info += section("Cookie Detail")
            for ck in r.cookies:
                info += (
                    f"  [accent]{ck.name}[/accent] = [value]{ck.value[:60]}[/value] "
                    f"[muted](domain={ck.domain}, secure={ck.secure})[/muted]\n"
                )

        print_result("Website Information", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 2 — HTTP SECURITY AUDIT
# ============================================================

def header_security_audit(url: str) -> None:
    """Full security header audit with pass/fail scoring."""
    url = ensure_url(url)
    try:
        with spinner("Auditing security headers...") as p:
            p.add_task("audit")
            r = requests.get(url, timeout=10, headers=HEADERS)

        checks = [
            ("Strict-Transport-Security",  "HSTS",                "Prevents protocol downgrade attacks",     True),
            ("Content-Security-Policy",    "CSP",                 "Mitigates XSS & data-injection attacks",  True),
            ("X-Frame-Options",            "X-Frame-Options",     "Prevents clickjacking",                   True),
            ("X-Content-Type-Options",     "X-Content-Type-Opt",  "Prevents MIME-type sniffing",             True),
            ("Referrer-Policy",            "Referrer-Policy",     "Controls referrer info leakage",          True),
            ("Permissions-Policy",         "Permissions-Policy",  "Restricts browser feature access",        True),
            ("Cross-Origin-Opener-Policy", "COOP",                "Prevents cross-origin window access",     True),
            ("Cross-Origin-Resource-Policy","CORP",               "Restricts cross-origin resource use",     True),
            ("Cross-Origin-Embedder-Policy","COEP",               "Controls cross-origin embedding",         True),
            ("X-XSS-Protection",           "X-XSS-Protection",   "Legacy browser XSS filter (deprecated)",  False),
        ]

        passed = 0
        total  = sum(1 for *_, req in checks if req)
        info   = section("Security Header Audit")

        for header, label, desc, required in checks:
            val = r.headers.get(header)
            if val:
                info += f"  [open]✔  PASS[/open]  [accent]{label}[/accent]\n"
                info += f"       [muted]{desc}[/muted]\n"
                info += f"       [value]{val[:90]}[/value]\n\n"
                if required:
                    passed += 1
            else:
                mark = "[danger]✘  FAIL[/danger]" if required else "[muted]—  N/A [/muted]"
                info += f"  {mark}  [accent]{label}[/accent]\n"
                info += f"       [muted]{desc} — MISSING[/muted]\n\n"

        score = int((passed / total) * 100) if total else 0
        if   score >= 80: score_str = f"[open]{score}% — GOOD[/open]"
        elif score >= 50: score_str = f"[warning]{score}% — NEEDS IMPROVEMENT[/warning]"
        else:             score_str = f"[danger]{score}% — POOR[/danger]"

        bar_filled = int(score / 5)
        bar        = "[open]" + "█" * bar_filled + "[/open]" + "[muted]" + "░" * (20 - bar_filled) + "[/muted]"

        info += section("Score")
        info += f"  {bar}  {score_str}\n"
        info += f"  [label]Passed:[/label] [value]{passed}/{total} required headers[/value]\n"

        print_result("HTTP Security Audit", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 3 — TECHNOLOGY DETECTION
# ============================================================

def tech_lookup(url: str) -> None:
    """Detect CMS, frameworks, CDN and tech stack via builtwith + header fingerprinting."""
    url = ensure_url(url)
    try:
        import builtwith

        with spinner("Detecting technologies...") as p:
            p.add_task("tech")
            tech = builtwith.parse(url)
            r    = requests.get(url, timeout=10, headers=HEADERS)

        info = ""
        if tech:
            info += section("Detected Stack (builtwith)")
            for cat, vals in sorted(tech.items()):
                info += f"  [cat]{cat}[/cat]\n"
                for v in vals:
                    info += f"    [accent]◆[/accent] [value]{v}[/value]\n"

        info += section("Header Fingerprints")
        fp_headers = {
            "X-Powered-By":      "Powered By",
            "X-Generator":       "Generator",
            "X-Drupal-Cache":    "Drupal",
            "X-WP-Total":        "WordPress REST",
            "X-Shopify-Stage":   "Shopify",
            "X-Magento-Tags":    "Magento",
            "CF-Ray":            "Cloudflare CDN",
            "X-Served-By":       "Served By",
            "X-Cache":           "Cache Layer",
            "Via":               "Proxy/CDN Via",
            "X-Varnish":         "Varnish Cache",
            "X-Nginx-Cache":     "Nginx Cache",
        }
        found_fp = False
        for hdr, label in fp_headers.items():
            val = r.headers.get(hdr)
            if val:
                info += f"  [open]✔[/open] [accent]{label}:[/accent] [value]{val}[/value]\n"
                found_fp = True
        if not found_fp:
            info += "  [muted]No technology fingerprint headers found[/muted]\n"

        # HTML-based hints
        soup = BeautifulSoup(r.text, "html.parser")
        gen  = soup.find("meta", attrs={"name": "generator"})
        if gen and gen.get("content"):
            info += section("HTML Generator Tag")
            info += f"  [accent]Generator:[/accent] [value]{gen['content']}[/value]\n"

        print_result("Technology Detection", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 4 — METADATA CRAWLER
# ============================================================

def metadata_crawler(url: str) -> None:
    """Extract all meta tags, Open Graph, Twitter Card, link tags, and external scripts."""
    url = ensure_url(url)
    try:
        with spinner("Crawling metadata...") as p:
            p.add_task("meta")
            r = requests.get(url, timeout=15, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        # Standard meta tags
        info  = section("Meta Tags")
        metas = soup.find_all("meta")
        if metas:
            for meta in metas:
                if meta.get("name"):
                    info += f"  [accent]name=[/accent][value]'{meta['name']}'[/value]  [label]content=[/label]'{meta.get('content','')[:100]}'\n"
                elif meta.get("property"):
                    info += f"  [accent]property=[/accent][value]'{meta['property']}'[/value]  [label]content=[/label]'{meta.get('content','')[:100]}'\n"
                elif meta.get("http-equiv"):
                    info += f"  [accent]http-equiv=[/accent][value]'{meta['http-equiv']}'[/value]  [label]content=[/label]'{meta.get('content','')[:100]}'\n"
        else:
            info += "  [muted]No meta tags found[/muted]\n"

        # Open Graph
        og_tags = soup.find_all("meta", property=re.compile(r"^og:"))
        if og_tags:
            info += section(f"Open Graph (og:) — {len(og_tags)} tags")
            for tag in og_tags:
                info += f"  [cat]{tag.get('property','')}[/cat]: [value]{tag.get('content','')[:120]}[/value]\n"

        # Twitter Card
        tw_tags = soup.find_all("meta", attrs={"name": re.compile(r"^twitter:")})
        if tw_tags:
            info += section(f"Twitter Card — {len(tw_tags)} tags")
            for tag in tw_tags:
                info += f"  [cat]{tag.get('name','')}[/cat]: [value]{tag.get('content','')[:120]}[/value]\n"

        # Link tags
        links = soup.find_all("link", rel=True)
        info += section(f"Link Tags ({len(links)})")
        for link in links[:20]:
            rel = " ".join(link.get("rel", []))
            href = link.get("href", "")[:80]
            info += f"  [accent]rel=[/accent][value]{rel}[/value]  [muted]{href}[/muted]\n"
        if len(links) > 20:
            info += f"  [muted]... and {len(links)-20} more[/muted]\n"

        # External scripts
        scripts = soup.find_all("script", src=True)
        info += section(f"External Scripts ({len(scripts)})")
        for s in scripts[:15]:
            info += f"  [muted]◆[/muted] [value]{s.get('src','')[:100]}[/value]\n"
        if len(scripts) > 15:
            info += f"  [muted]... and {len(scripts)-15} more[/muted]\n"

        print_result("Metadata Crawler", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 5 — ROBOTS.TXT & SITEMAP
# ============================================================

def robots_sitemap(url: str) -> None:
    """Read robots.txt, sitemap.xml, and sitemap_index.xml."""
    base_url = ensure_url(clean_domain(url))
    parsed   = urlparse(base_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    info = ""
    for path in ["/robots.txt", "/sitemap.xml", "/sitemap_index.xml"]:
        try:
            r = requests.get(base_url + path, timeout=8, headers=HEADERS)
            if r.status_code == 200:
                content = r.text.strip()
                info += section(f"{path}  ({len(content):,} bytes  |  HTTP {r.status_code})")
                lines = content.split("\n")
                for line in lines[:60]:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("#"):
                        info += f"  [muted]{line}[/muted]\n"
                    elif ":" in line:
                        k, v = line.split(":", 1)
                        info += f"  [accent]{k}:[/accent] [value]{v.strip()}[/value]\n"
                    else:
                        info += f"  [value]{line}[/value]\n"
                if len(lines) > 60:
                    info += f"  [muted]... truncated — {len(lines)} total lines[/muted]\n"
            else:
                info += section(path)
                info += f"  [muted]Not found — HTTP {r.status_code}[/muted]\n"
        except Exception as e:
            info += section(path)
            info += f"  [danger]Error: {e}[/danger]\n"

    print_result("Robots.txt & Sitemap", info, subtitle=base_url)


# ============================================================
# 6 — EMAIL / CONTACT HARVESTER
# ============================================================

def email_harvester(url: str) -> None:
    """Extract emails, phone numbers, and social media links from a webpage."""
    url = ensure_url(url)
    try:
        with spinner("Harvesting contacts...") as p:
            p.add_task("harvest")
            r = requests.get(url, timeout=15, headers=HEADERS)

        soup = BeautifulSoup(r.text, "html.parser")
        text = r.text

        # Emails
        raw_emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
        bad_exts   = (".png", ".jpg", ".gif", ".css", ".js", ".svg", ".woff")
        emails     = sorted({e for e in raw_emails if not any(e.endswith(x) for x in bad_exts)})

        # Phones
        raw_phones = re.findall(r"\+?[\d\s\-\(\)]{10,18}", text)
        phones     = sorted({p.strip() for p in raw_phones if len(re.sub(r"\D", "", p)) >= 9})[:20]

        # Social media
        socials: dict[str, list[str]] = {
            "facebook.com": [], "twitter.com": [], "x.com": [],
            "instagram.com": [], "linkedin.com": [], "github.com": [],
            "youtube.com": [], "tiktok.com": [], "t.me": [],
        }
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for platform in socials:
                if platform in href and href not in socials[platform]:
                    socials[platform].append(href)

        info  = section(f"Email Addresses ({len(emails)})")
        if emails:
            for email in emails[:30]:
                info += f"  [open]✉[/open]  [value]{email}[/value]\n"
            if len(emails) > 30:
                info += f"  [muted]... and {len(emails)-30} more[/muted]\n"
        else:
            info += "  [muted]No email addresses found[/muted]\n"

        if phones:
            info += section(f"Phone Numbers ({len(phones)})")
            for phone in phones[:15]:
                info += f"  [accent]📞[/accent]  [value]{phone}[/value]\n"

        info += section("Social Media Links")
        any_social = False
        for platform, links in socials.items():
            if links:
                any_social = True
                for link in links[:3]:
                    info += f"  [cat]{platform}:[/cat] [value]{link[:100]}[/value]\n"
        if not any_social:
            info += "  [muted]No social media links found[/muted]\n"

        print_result("Email & Contact Harvester", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ============================================================
# 7 — FULL WEBSITE RECON (COMBO)
# ============================================================

def website_recon(url: str) -> None:
    """Run Website Info + Security Audit + SSL + Tech Detection in sequence."""
    url = ensure_url(url)
    console.print(Rule(f"[{TITLE_STYLE}]◈ Full Website Recon: {url} ◈[/{TITLE_STYLE}]", style=BORDER_STYLE))
    website_info(url)
    console.print()
    header_security_audit(url)
    console.print()
    tech_lookup(url)
