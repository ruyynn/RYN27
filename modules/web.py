#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/web.py
Web recon features: website info, security audit, tech detection,
metadata crawler, robots/sitemap, email harvester, full recon combo.
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from rich.rule import Rule

from modules.core import (
    console, ensure_url, clean_domain, print_result, section, spinner,
    TITLE_STYLE, BORDER_STYLE
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. WEBSITE INFORMATION
# ─────────────────────────────────────────────────────────────────────────────

def website_info(url: str):
    """HTTP headers, status code, title, description, redirect chain, security headers."""
    url = ensure_url(url)
    try:
        with spinner("Fetching website info...") as p:
            p.add_task("fetch")
            start   = time.time()
            session = requests.Session()
            r = session.get(
                url, timeout=15, allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
            )
            elapsed = time.time() - start

        soup      = BeautifulSoup(r.text, "html.parser")
        title_tag = soup.find("title")
        desc_tag  = soup.find("meta", attrs={"name": "description"})
        gen_tag   = soup.find("meta", attrs={"name": "generator"})

        sc = r.status_code
        if sc < 300:
            sc_str = f"[open]{sc} OK[/open]"
        elif sc < 400:
            sc_str = f"[warning]{sc} REDIRECT[/warning]"
        else:
            sc_str = f"[danger]{sc} ERROR[/danger]"

        info  = section("General")
        info += f"[label]URL          :[/label] [value]{r.url}[/value]\n"
        info += f"[label]Status Code  :[/label] {sc_str}\n"
        info += f"[label]Response Time:[/label] [accent]{elapsed:.3f}s[/accent]\n"
        info += f"[label]Title        :[/label] [value]{title_tag.text.strip() if title_tag else 'N/A'}[/value]\n"
        info += f"[label]Description  :[/label] [value]{desc_tag['content'][:120] if desc_tag and desc_tag.get('content') else 'N/A'}[/value]\n"
        info += f"[label]Generator    :[/label] [value]{gen_tag['content'] if gen_tag and gen_tag.get('content') else 'N/A'}[/value]\n"
        info += f"[label]Content-Type :[/label] [value]{r.headers.get('Content-Type', 'N/A')}[/value]\n"
        info += f"[label]Server       :[/label] [value]{r.headers.get('Server', 'N/A')}[/value]\n"
        info += f"[label]Cookies      :[/label] [accent]{len(r.cookies)} found[/accent]\n"
        info += f"[label]Content-Len  :[/label] [value]{len(r.content):,} bytes[/value]\n"

        # Redirect chain
        if r.history:
            info += section("Redirect Chain")
            for redir in r.history:
                info += f"  [muted]→[/muted] [warning]{redir.status_code}[/warning] [value]{redir.url}[/value]\n"
            info += f"  [muted]→[/muted] [open]{r.status_code}[/open] [value]{r.url}[/value]\n"

        # Quick security header summary
        sec_headers = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy":   "CSP",
            "X-Frame-Options":           "X-Frame-Options",
            "X-Content-Type-Options":    "X-Content-Type-Options",
            "Referrer-Policy":           "Referrer-Policy",
            "Permissions-Policy":        "Permissions-Policy",
        }
        info += section("Security Headers (quick)")
        for hdr, lbl in sec_headers.items():
            val = r.headers.get(hdr)
            if val:
                info += f"  [open]✔[/open] [accent]{lbl}[/accent]: [muted]{val[:60]}[/muted]\n"
            else:
                info += f"  [closed]✘[/closed] [muted]{lbl}: missing[/muted]\n"

        # All HTTP headers
        info += section("HTTP Headers")
        for h, v in r.headers.items():
            info += f"  [accent]{h}:[/accent] [value]{v}[/value]\n"

        # Cookie details
        if r.cookies:
            info += section("Cookies Detail")
            for ck in r.cookies:
                info += (
                    f"  [accent]{ck.name}[/accent] = [value]{ck.value[:60]}[/value] "
                    f"[muted](domain={ck.domain}, secure={ck.secure})[/muted]\n"
                )

        print_result("Website Information", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 2. HTTP SECURITY AUDIT
# ─────────────────────────────────────────────────────────────────────────────

def header_security_audit(url: str):
    """Detailed audit of HTTP security headers with pass/fail scoring."""
    url = ensure_url(url)
    try:
        with spinner("Auditing security headers...") as p:
            p.add_task("audit")
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})

        checks = [
            ("Strict-Transport-Security",   "HSTS",                "Prevents HTTPS downgrade attacks",      True),
            ("Content-Security-Policy",      "CSP",                 "Prevents XSS & injection attacks",       True),
            ("X-Frame-Options",              "X-Frame-Options",     "Prevents clickjacking",                  True),
            ("X-Content-Type-Options",       "X-Content-Type-Opt",  "Prevents MIME-type sniffing",            True),
            ("Referrer-Policy",              "Referrer-Policy",     "Controls referrer info leakage",         True),
            ("Permissions-Policy",           "Permissions-Policy",  "Controls browser feature access",        True),
            ("X-XSS-Protection",             "X-XSS-Protection",   "Legacy XSS filter (deprecated but ok)",  False),
            ("Cross-Origin-Opener-Policy",   "COOP",                "Prevents cross-origin leaks",            True),
            ("Cross-Origin-Resource-Policy", "CORP",                "Controls resource sharing",              True),
            ("Cross-Origin-Embedder-Policy", "COEP",                "Controls cross-origin embedding",        True),
        ]

        passed = 0
        total  = sum(1 for *_, req in checks if req)
        info   = section("Header Audit Results")

        for header, lbl, desc, required in checks:
            val = r.headers.get(header)
            if val:
                info += f"  [open]✔  PASS[/open]  [accent]{lbl}[/accent]\n"
                info += f"       [muted]{desc}[/muted]\n"
                info += f"       [value]{val[:90]}[/value]\n\n"
                if required:
                    passed += 1
            else:
                mark = "[danger]✘  FAIL[/danger]" if required else "[muted]—  N/A [/muted]"
                info += f"  {mark}  [accent]{lbl}[/accent]\n"
                info += f"       [muted]{desc} — MISSING[/muted]\n\n"

        score = int((passed / total) * 100) if total else 0
        if score >= 80:
            score_str = f"[open]{score}% — GOOD[/open]"
        elif score >= 50:
            score_str = f"[warning]{score}% — NEEDS IMPROVEMENT[/warning]"
        else:
            score_str = f"[danger]{score}% — POOR[/danger]"

        info += section("Overall Score")
        info += f"  [label]Security Score :[/label] {score_str}\n"
        info += f"  [label]Headers Passed :[/label] [value]{passed}/{total} required[/value]\n"

        if score < 60:
            info += (
                f"\n  [warning]⚠  Recommendation:[/warning] [muted]This site is missing critical "
                f"security headers. Implement HSTS, CSP, and X-Frame-Options at minimum.[/muted]\n"
            )

        print_result("HTTP Security Audit", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 3. TECHNOLOGY DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def tech_lookup(url: str):
    """Detect CMS, frameworks, CDN, analytics via builtwith + header fingerprinting."""
    import builtwith
    url = ensure_url(url)
    try:
        with spinner("Detecting technologies...") as p:
            p.add_task("tech")
            tech = builtwith.parse(url)
            r    = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})

        info = ""

        if tech:
            info += section("Detected Stack (builtwith)")
            for cat, vals in sorted(tech.items()):
                info += f"  [cat]{cat}[/cat]\n"
                for v in vals:
                    info += f"    [accent]◆[/accent] [value]{v}[/value]\n"
        else:
            info += section("Detected Stack")
            info += "  [muted]No technologies detected via builtwith[/muted]\n"

        # Header fingerprinting
        fingerprint_headers = {
            "X-Powered-By":      "Powered By",
            "X-Generator":       "Generator",
            "X-Drupal-Cache":    "Drupal",
            "X-WP-Total":        "WordPress API",
            "X-Shopify-Stage":   "Shopify",
            "X-Magento-Tags":    "Magento",
            "CF-Ray":            "Cloudflare",
            "X-Served-By":       "Served By",
            "X-Cache":           "Cache Layer",
            "Via":               "Via Proxy",
            "X-Varnish":         "Varnish Cache",
            "X-Litespeed-Cache": "LiteSpeed Cache",
        }
        info += section("Header Fingerprints")
        found_any = False
        for hdr, lbl in fingerprint_headers.items():
            val = r.headers.get(hdr)
            if val:
                info += f"  [open]✔[/open] [accent]{lbl}:[/accent] [value]{val[:80]}[/value]\n"
                found_any = True
        if not found_any:
            info += "  [muted]No fingerprint headers detected[/muted]\n"

        # HTML-based clues
        soup = BeautifulSoup(r.text, "html.parser")
        gen  = soup.find("meta", attrs={"name": "generator"})
        if gen and gen.get("content"):
            info += section("HTML Meta Generator")
            info += f"  [open]✔[/open] [accent]{gen['content']}[/accent]\n"

        print_result("Technology Detection", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 4. METADATA CRAWLER
# ─────────────────────────────────────────────────────────────────────────────

def metadata_crawler(url: str):
    """Extract all meta tags, Open Graph, Twitter Card, link tags, external scripts."""
    url = ensure_url(url)
    try:
        with spinner("Crawling metadata...") as p:
            p.add_task("meta")
            r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        info  = section("Meta Tags")
        metas = soup.find_all("meta")
        if metas:
            for meta in metas:
                if meta.get("name"):
                    info += (
                        f"  [accent]name=[/accent][value]'{meta['name']}'[/value]  "
                        f"[label]content=[/label]'{meta.get('content','')[:100]}'\n"
                    )
                elif meta.get("property"):
                    info += (
                        f"  [accent]property=[/accent][value]'{meta['property']}'[/value]  "
                        f"[label]content=[/label]'{meta.get('content','')[:100]}'\n"
                    )
                elif meta.get("http-equiv"):
                    info += (
                        f"  [accent]http-equiv=[/accent][value]'{meta['http-equiv']}'[/value]  "
                        f"[label]content=[/label]'{meta.get('content','')[:100]}'\n"
                    )
        else:
            info += "  [muted]No meta tags found[/muted]\n"

        # Open Graph
        og_tags = soup.find_all("meta", property=re.compile(r"^og:"))
        if og_tags:
            info += section(f"Open Graph ({len(og_tags)} tags)")
            for tag in og_tags:
                info += f"  [cat]{tag.get('property','')}[/cat]: [value]{tag.get('content','')[:100]}[/value]\n"

        # Twitter Card
        tw_tags = soup.find_all("meta", attrs={"name": re.compile(r"^twitter:")})
        if tw_tags:
            info += section(f"Twitter Card ({len(tw_tags)} tags)")
            for tag in tw_tags:
                info += f"  [cat]{tag.get('name','')}[/cat]: [value]{tag.get('content','')[:100]}[/value]\n"

        # Link tags
        links = soup.find_all("link", rel=True)
        info += section(f"Link Tags ({len(links)})")
        for link in links[:15]:
            info += (
                f"  [accent]rel=[/accent][value]{' '.join(link.get('rel',[]))}[/value] "
                f"[muted]href={link.get('href','')[:80]}[/muted]\n"
            )

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


# ─────────────────────────────────────────────────────────────────────────────
# 5. ROBOTS.TXT & SITEMAP
# ─────────────────────────────────────────────────────────────────────────────

def robots_sitemap(url: str):
    """Fetch and display robots.txt, sitemap.xml, sitemap_index.xml."""
    from urllib.parse import urlparse
    base    = ensure_url(clean_domain(url))
    parsed  = urlparse(base)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    info = ""
    for path in ["/robots.txt", "/sitemap.xml", "/sitemap_index.xml"]:
        try:
            r = requests.get(base_url + path, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                content = r.text.strip()
                info += section(f"{path}  ({len(content):,} bytes)")
                lines = content.split("\n")
                for line in lines[:60]:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("#"):
                        info += f"  [muted]{line}[/muted]\n"
                    elif ":" in line:
                        parts = line.split(":", 1)
                        info += f"  [accent]{parts[0]}:[/accent] [value]{parts[1].strip()}[/value]\n"
                    else:
                        info += f"  [value]{line}[/value]\n"
                if len(lines) > 60:
                    info += f"  [muted]... truncated ({len(lines)} total lines)[/muted]\n"
            else:
                info += section(path)
                info += f"  [muted]Not found — HTTP {r.status_code}[/muted]\n"
        except Exception as e:
            info += section(path)
            info += f"  [danger]Error: {e}[/danger]\n"

    print_result("Robots.txt & Sitemap", info, subtitle=base_url)


# ─────────────────────────────────────────────────────────────────────────────
# 6. EMAIL / CONTACT HARVESTER
# ─────────────────────────────────────────────────────────────────────────────

def email_harvester(url: str):
    """Extract emails, phone numbers, and social media links from a web page."""
    url = ensure_url(url)
    try:
        with spinner("Harvesting contacts...") as p:
            p.add_task("harvest")
            r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(r.text, "html.parser")
        text = r.text

        # Emails
        emails = sorted(set(re.findall(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text
        )))
        emails = [e for e in emails if not any(
            e.endswith(x) for x in [".png", ".jpg", ".css", ".js", ".svg", ".gif"]
        )]

        # Phones
        raw_phones = re.findall(r"\+?[\d\s\-\(\)]{9,17}", text)
        phones = sorted(set(
            p.strip() for p in raw_phones
            if len(re.sub(r"\D", "", p)) >= 9
        ))[:20]

        # Social links
        platforms = {
            "facebook.com": [], "twitter.com": [], "x.com": [],
            "instagram.com": [], "linkedin.com": [], "github.com": [],
            "youtube.com": [], "tiktok.com": [], "t.me": [],
        }
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for pf in platforms:
                if pf in href and href not in platforms[pf]:
                    platforms[pf].append(href)

        info = section(f"Email Addresses ({len(emails)})")
        if emails:
            for email in emails[:30]:
                info += f"  [open]✉[/open]  [value]{email}[/value]\n"
        else:
            info += "  [muted]No email addresses found[/muted]\n"

        if phones:
            info += section(f"Phone Numbers ({len(phones)})")
            for phone in phones[:15]:
                info += f"  [accent]📞[/accent]  [value]{phone}[/value]\n"

        info += section("Social Media Links")
        any_social = False
        for pf, links in platforms.items():
            if links:
                any_social = True
                for link in links[:3]:
                    info += f"  [cat]{pf}[/cat]  [value]{link[:90]}[/value]\n"
        if not any_social:
            info += "  [muted]No social media links detected[/muted]\n"

        print_result("Email & Contact Harvester", info, subtitle=url)

    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")


# ─────────────────────────────────────────────────────────────────────────────
# 7. FULL WEBSITE RECON (COMBO)
# ─────────────────────────────────────────────────────────────────────────────

def website_recon(url: str):
    """Run website_info + SSL + tech_lookup in one pass."""
    from modules.ssl_module import ssl_info
    url = ensure_url(url)
    console.print(Rule(
        f"[{TITLE_STYLE}]  ⚡  Full Website Recon: {url}  ⚡  [/{TITLE_STYLE}]",
        style=BORDER_STYLE
    ))
    website_info(url)
    console.print()
    ssl_info(url)
    console.print()
    tech_lookup(url)
    console.print()
    header_security_audit(url)
