#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — core.py
Theme, color detection, console, logos, shared helpers.
"""

import os
import sys
import re
import socket
from urllib.parse import urlparse

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.align import Align

# ============================================================
# VERSION
# ============================================================
VERSION = "1.8.0"
REPO_URL = "https://github.com/ruyynn/RYN27"
AUTHOR   = "Ruyynn"

# ============================================================
# CROSS-PLATFORM COLOR DETECTION
# ============================================================

def detect_color_support():
    """Detect truecolor / 256 / none across Linux, Windows, macOS, Termux."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
        if os.environ.get("WT_SESSION") or os.environ.get("COLORTERM") in ("truecolor", "24bit"):
            return "truecolor"
        return "256"

    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return "truecolor"

    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    if term_program in ("iterm.app", "hyper", "vscode", "wezterm"):
        return "truecolor"
    if term_program == "apple_terminal":
        return "256"

    term = os.environ.get("TERM", "").lower()
    if "256color" in term or "256colour" in term:
        return "256"
    if term in ("xterm", "screen", "tmux"):
        return "256"

    if os.environ.get("PREFIX") and "com.termux" in os.environ.get("PREFIX", ""):
        return "256"

    if not sys.stdout.isatty():
        return "none"

    return "256"


COLOR_LEVEL = detect_color_support()

# ============================================================
# THEME — degrades gracefully per color level
# ============================================================

if COLOR_LEVEL == "truecolor":
    THEME = Theme({
        "primary":   "bold #00D4FF",
        "secondary": "bold #BF5FFF",
        "accent":    "bold #00FF9F",
        "warning":   "bold #FFD700",
        "danger":    "bold #FF4560",
        "muted":     "#6C7A89",
        "success":   "bold #00E676",
        "title":     "bold #FF6B9D",
        "border":    "#00D4FF",
        "label":     "bold #E0E0E0",
        "value":     "#B0BEC5",
        "logo1":     "bold #CE1126",
        "logo2":     "bold #FFFFFF",
        "logo3":     "bold #CE1126",
        "logo4":     "bold #FFFFFF",
        "logo5":     "bold #CE1126",
        "logo6":     "bold #FFFFFF",
        "logo7":     "bold #CE1126",
        "star":      "bold #FFD700",
        "info":      "bold #29B6F6",
        "cat":       "bold #AB47BC",
        "open":      "bold #00E676",
        "closed":    "bold #FF4560",
        "section":   "bold #00D4FF",
    })
    BORDER_STYLE   = "#00D4FF"
    PANEL_BORDER   = "#BF5FFF"
    TITLE_STYLE    = "bold #FF6B9D"
    MENU_OPT_STYLE = "bold #FFD700"
    MENU_FN_STYLE  = "bold #E0E0E0"
    MENU_CAT_STYLE = "bold #00FF9F"
    PROMPT_STYLE   = "bold #FFD700"
    INPUT_STYLE    = "bold #00D4FF"
    EXIT_STYLE     = "bold #00E676"
    LOGO_COLORS    = ["logo1","logo2","logo3","logo4","logo5","logo6","logo7"]

elif COLOR_LEVEL == "256":
    THEME = Theme({
        "primary":   "bold cyan",
        "secondary": "bold magenta",
        "accent":    "bold green",
        "warning":   "bold yellow",
        "danger":    "bold red",
        "muted":     "bright_black",
        "success":   "bold bright_green",
        "title":     "bold bright_magenta",
        "border":    "cyan",
        "label":     "bold white",
        "value":     "bright_white",
        "logo1":     "bold red",
        "logo2":     "bold white",
        "logo3":     "bold red",
        "logo4":     "bold white",
        "logo5":     "bold red",
        "logo6":     "bold white",
        "logo7":     "bold red",
        "star":      "bold yellow",
        "info":      "bold cyan",
        "cat":       "bold magenta",
        "open":      "bold bright_green",
        "closed":    "bold red",
        "section":   "bold cyan",
    })
    BORDER_STYLE   = "cyan"
    PANEL_BORDER   = "magenta"
    TITLE_STYLE    = "bold bright_magenta"
    MENU_OPT_STYLE = "bold bright_yellow"
    MENU_FN_STYLE  = "bold white"
    MENU_CAT_STYLE = "bold bright_green"
    PROMPT_STYLE   = "bold bright_yellow"
    INPUT_STYLE    = "bold cyan"
    EXIT_STYLE     = "bold bright_green"
    LOGO_COLORS    = ["logo1","logo2","logo3","logo4","logo5","logo6","logo7"]

else:
    THEME = Theme({
        "primary": "bold", "secondary": "bold", "accent": "bold",
        "warning": "bold", "danger": "bold", "muted": "",
        "success": "bold", "title": "bold", "border": "white",
        "label": "bold", "value": "", "info": "bold", "cat": "bold",
        "open": "bold", "closed": "bold", "section": "bold",
        "logo1": "bold", "logo2": "bold", "logo3": "bold",
        "logo4": "bold", "logo5": "bold", "logo6": "bold", "logo7": "bold",
        "star": "bold",
    })
    BORDER_STYLE   = "white"
    PANEL_BORDER   = "white"
    TITLE_STYLE    = "bold"
    MENU_OPT_STYLE = "bold"
    MENU_FN_STYLE  = "bold"
    MENU_CAT_STYLE = "bold"
    PROMPT_STYLE   = "bold"
    INPUT_STYLE    = "bold"
    EXIT_STYLE     = "bold"
    LOGO_COLORS    = ["logo1"] * 7

# Global console
console = Console(theme=THEME)

# ============================================================
# LOGO UTAMA RYN27 — MERAH-PUTIH (BENDERA INDONESIA)
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
    """Cetak logo seperti bendera Indonesia — merah atas, putih bawah."""
    lines = LOGO_MAIN.split('\n')
    content_lines = [l for l in lines if l.strip()]
    total = len(content_lines)
    half  = total // 2
    for idx, line in enumerate(content_lines):
        if idx < half:
            if COLOR_LEVEL == "truecolor":
                console.print(f"[bold #CE1126]{line}[/bold #CE1126]")
            elif COLOR_LEVEL == "256":
                console.print(f"[bold red]{line}[/bold red]")
            else:
                console.print(f"[bold]{line}[/bold]")
        else:
            if COLOR_LEVEL == "truecolor":
                console.print(f"[bold #FFFFFF]{line}[/bold #FFFFFF]")
            elif COLOR_LEVEL == "256":
                console.print(f"[bold white]{line}[/bold white]")
            else:
                console.print(f"[bold]{line}[/bold]")

# ============================================================
# LOGO BINTANG — DIPERTAHANKAN
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
# SHARED HELPERS
# ============================================================

def get_ip_from_domain(domain: str):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None

def clean_domain(target: str) -> str:
    """Strip protocol & path, return bare hostname."""
    target = target.strip().rstrip('/')
    if "://" in target:
        target = urlparse(target).netloc or target
    return target

def ensure_url(target: str) -> str:
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        return 'https://' + target
    return target

def is_ip(target: str) -> bool:
    return bool(re.match(r'^\d{1,3}(\.\d{1,3}){3}$', target))

def print_result(title: str, data: str, subtitle: str = None):
    """Render a rich Panel with optional subtitle."""
    title_str = f"[{TITLE_STYLE}]{title}[/{TITLE_STYLE}]"
    if subtitle:
        title_str += f" [muted]— {subtitle}[/muted]"
    console.print(Panel(
        data,
        title=title_str,
        border_style=PANEL_BORDER,
        title_align="left",
        padding=(1, 2)
    ))

def section(label: str) -> str:
    """Inline section divider string for use inside panel text."""
    return f"\n[section]{'─' * 4} {label} {'─' * 4}[/section]\n"

def spinner(msg: str):
    """Return a transient Progress spinner context manager."""
    return Progress(
        SpinnerColumn(style="primary"),
        TextColumn(f"[primary]{msg}[/primary]"),
        transient=True,
        console=console
    )

def print_header():
    """Print logo + version bar."""
    print_gradient_logo()
    console.print(
        Align.center(
            f"[primary]v{VERSION}[/primary]  "
            f"[muted]|[/muted]  "
            f"[secondary]{REPO_URL}[/secondary]  "
            f"[muted]|[/muted]  "
            f"[warning]for educational & authorized use only[/warning]"
        )
    )
    console.print()
