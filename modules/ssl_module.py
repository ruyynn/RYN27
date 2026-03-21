#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/ssl_module.py
SSL/TLS certificate inspection.
"""

import ssl
import socket
from datetime import datetime

from modules.core import (
    console, clean_domain, print_result, section, spinner
)


# ─────────────────────────────────────────────────────────────────────────────
# 19. SSL / TLS CERTIFICATE INSPECTOR
# ─────────────────────────────────────────────────────────────────────────────

def ssl_info(target: str):
    """
    Connect to port 443 and inspect the TLS certificate:
    subject, issuer, validity, SAN list, cipher suite.
    """
    domain = clean_domain(target)
    try:
        with spinner(f"Fetching SSL/TLS cert for {domain}...") as p:
            p.add_task("ssl")
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
                socket.create_connection((domain, 443), timeout=10),
                server_hostname=domain
            ) as ssock:
                cert     = ssock.getpeercert()
                protocol = ssock.version()
                cipher   = ssock.cipher()

        subject    = dict(x[0] for x in cert.get("subject", []))
        issuer     = dict(x[0] for x in cert.get("issuer", []))
        not_before = cert.get("notBefore", "N/A")
        not_after  = cert.get("notAfter",  "N/A")
        san        = cert.get("subjectAltName", [])

        # Expiry countdown
        try:
            exp_dt    = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            days_left = (exp_dt - datetime.utcnow()).days
            if days_left > 30:
                exp_str = f"[open]{not_after} ({days_left}d left)[/open]"
            elif days_left > 0:
                exp_str = f"[warning]{not_after} ({days_left}d left — EXPIRING SOON)[/warning]"
            else:
                exp_str = f"[danger]{not_after} — EXPIRED[/danger]"
        except Exception:
            exp_str = not_after

        info  = section("Certificate")
        info += f"[label]Common Name  :[/label] [value]{subject.get('commonName', 'N/A')}[/value]\n"
        info += f"[label]Organization :[/label] [value]{subject.get('organizationName', 'N/A')}[/value]\n"
        info += f"[label]Valid From   :[/label] [value]{not_before}[/value]\n"
        info += f"[label]Valid Until  :[/label] {exp_str}\n"
        info += f"[label]Serial No.   :[/label] [muted]{cert.get('serialNumber', 'N/A')}[/muted]\n"

        info += section("Issuer")
        info += f"[label]Issuer CN    :[/label] [value]{issuer.get('commonName', 'N/A')}[/value]\n"
        info += f"[label]Issuer Org   :[/label] [value]{issuer.get('organizationName', 'N/A')}[/value]\n"
        info += f"[label]Issuer Ctry  :[/label] [value]{issuer.get('countryName', 'N/A')}[/value]\n"

        info += section("TLS")
        info += f"[label]Protocol     :[/label] [accent]{protocol}[/accent]\n"
        info += f"[label]Cipher Suite :[/label] [value]{cipher[0] if cipher else 'N/A'}[/value]\n"
        info += f"[label]Key Bits     :[/label] [value]{cipher[2] if cipher else 'N/A'}[/value]\n"

        if san:
            info += section(f"Subject Alt Names ({len(san)})")
            for _, name in san[:25]:
                info += f"  [accent]◆[/accent] [value]{name}[/value]\n"
            if len(san) > 25:
                info += f"  [muted]... and {len(san) - 25} more[/muted]\n"

        print_result("SSL/TLS Certificate", info, subtitle=domain)

    except ssl.SSLCertVerificationError as e:
        console.print(f"[danger]SSL Verification Error: {e}[/danger]")
    except ssl.SSLError as e:
        console.print(f"[danger]SSL Error: {e}[/danger]")
    except ConnectionRefusedError:
        console.print(f"[danger]Port 443 is closed on {domain}[/danger]")
    except Exception as e:
        console.print(f"[danger]Error: {e}[/danger]")
