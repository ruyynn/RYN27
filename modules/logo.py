#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RYN27 — modules/logo.py
ASCII art logos — main gradient logo (red-white Indonesian flag)
and star logo. Both are preserved exactly as original.
"""

from rich.align import Align
from modules.theme import console, COLOR_LEVEL, TITLE_STYLE
from modules.utils import VERSION, GITHUB_USER

# ============================================================
# LOGO UTAMA RYN27 — MERAH-PUTIH (DIPERTAHANKAN)
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
# PRINT FUNCTIONS
# ============================================================

def print_gradient_logo() -> None:
    """Print main logo with Indonesian flag gradient (red top / white bottom)."""
    lines = LOGO_MAIN.split("\n")
    content_lines = [l for l in lines if l.strip()]
    total = len(content_lines)
    half  = total // 2

    for idx, line in enumerate(content_lines):
        if idx < half:
            # Upper half — RED
            if COLOR_LEVEL == "truecolor":
                console.print(f"[bold #CE1126]{line}[/bold #CE1126]")
            elif COLOR_LEVEL == "256":
                console.print(f"[bold red]{line}[/bold red]")
            else:
                console.print(f"[bold]{line}[/bold]")
        else:
            # Lower half — WHITE
            if COLOR_LEVEL == "truecolor":
                console.print(f"[bold #FFFFFF]{line}[/bold #FFFFFF]")
            elif COLOR_LEVEL == "256":
                console.print(f"[bold white]{line}[/bold white]")
            else:
                console.print(f"[bold]{line}[/bold]")


def print_header() -> None:
    """Print logo + version tagline."""
    print_gradient_logo()
    console.print(
        Align.center(
            f"[primary]v{VERSION}[/primary]  "
            f"[muted]|[/muted]  "
            f"[secondary]{GITHUB_USER}[/secondary]  "
            f"[muted]|[/muted]  "
            f"[warning]for educational & authorized use only[/warning]"
        )
    )
    console.print()
