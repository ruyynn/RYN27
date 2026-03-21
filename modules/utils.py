#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/utils.py
Shared utility functions used across all feature modules.
"""

import socket
import re
from urllib.parse import urlparse

from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from modules.theme import console, TITLE_STYLE, PANEL_BORDER

# ============================================================
# CONSTANTS
# ============================================================

VERSION     = "1.8.0"
AUTHOR      = "Ruyynn"
GITHUB_URL  = "https://github.com/ruyynn/RYN27"
GITHUB_USER = "github.com/ruyynn"

# ============================================================
# TARGET HELPERS
# ============================================================

def get_ip_from_domain(domain: str) -> str | None:
    """Resolve domain to IPv4 address."""
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def clean_domain(target: str) -> str:
    """Strip protocol and path, return bare hostname."""
    target = target.strip()
    if "://" in target:
        parsed = urlparse(target)
        target = parsed.netloc or target
    return target.rstrip("/").strip()


def ensure_url(target: str) -> str:
    """Ensure target has https:// scheme."""
    target = target.strip()
    if not target.startswith(("http://", "https://")):
        return "https://" + target
    return target


def is_ip(target: str) -> bool:
    """Return True if target looks like an IPv4 address."""
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", target))

# ============================================================
# OUTPUT HELPERS
# ============================================================

def print_result(title: str, data: str, subtitle: str = None) -> None:
    """Display results inside a premium-styled Rich panel."""
    title_str = f"[{TITLE_STYLE}]{title}[/{TITLE_STYLE}]"
    if subtitle:
        short = subtitle[:60] + "…" if len(subtitle) > 60 else subtitle
        title_str += f" [muted]— {short}[/muted]"
    panel = Panel(
        data,
        title=title_str,
        border_style=PANEL_BORDER,
        title_align="left",
        padding=(1, 2),
    )
    console.print(panel)


def section(label: str) -> str:
    """Return a mini section divider string for use inside panel text."""
    return f"\n[section]{'─' * 4} {label} {'─' * 4}[/section]\n"


def spinner(msg: str) -> Progress:
    """Return a transient spinner Progress context manager."""
    return Progress(
        SpinnerColumn(style="primary"),
        TextColumn(f"[primary]{msg}[/primary]"),
        transient=True,
        console=console,
    )
