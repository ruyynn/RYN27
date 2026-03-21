#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/theme.py
Cross-platform color detection, theme, and shared console instance.
"""

import os
import sys
from rich.console import Console
from rich.theme import Theme

# ============================================================
# CROSS-PLATFORM COLOR DETECTION
# ============================================================

def detect_color_support():
    """
    Detect terminal color capability across Linux, Windows, macOS, Termux.
    Returns: 'truecolor', '256', 'basic', or 'none'
    """
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
        "cta":       "bold #FFD700",
        "link":      "bold #00D4FF underline",
        "hi":        "bold #FF6B9D",
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
        "cta":       "bold yellow",
        "link":      "bold cyan underline",
        "hi":        "bold bright_magenta",
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
        "cta": "bold", "link": "bold underline", "hi": "bold",
        "logo1": "bold", "logo2": "bold", "logo3": "bold",
        "logo4": "bold", "logo5": "bold", "logo6": "bold", "logo7": "bold",
        "star":  "bold",
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

# Shared console instance — import this everywhere
console = Console(theme=THEME)
