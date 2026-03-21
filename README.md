# RYN27 — Ultimate Information Gathering Tool

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/Version-1.8.0-CE1126?style=for-the-badge&logo=git&logoColor=white)](https://github.com/ruyynn/RYN27/releases)
[![License](https://img.shields.io/badge/License-MIT-2ecc71?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ruyynn/RYN27?style=for-the-badge&logo=github&logoColor=white&color=f1c40f)](https://github.com/ruyynn/RYN27/stargazers)
[![Issues](https://img.shields.io/github/issues/ruyynn/RYN27?style=for-the-badge&logo=githubactions&logoColor=white&color=e74c3c)](https://github.com/ruyynn/RYN27/issues)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-555?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/ruyynn/RYN27)

> **RYN27** is a CLI-based OSINT and information-gathering tool that combines WHOIS, DNS enumeration, port scanning, IP geolocation, SSL inspection, technology detection, and full web recon into a single clean and premium terminal interface.
> Built for **security researchers**, **bug bounty hunters**, **CTF players**, and **sysadmins** who need a fast, lightweight, no-nonsense recon tool — runs on Linux, macOS, Windows, and Android (Termux).

---

## 📸 Screenshot

<p>
  <img src="assets/demo.svg" width="80%"/>
  <img src="assets/preview.png" width="80%"/>
</p>

---

## ⭐ If this tool helped you, drop a star — it keeps the project alive!

[![Star this repo](https://img.shields.io/badge/⭐%20Star%20this%20repo-FFD700?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ruyynn/RYN27)

---

## ✨ Features

### 🌐 Web Recon
| # | Feature | Description |
|---|---------|-------------|
| 1 | **Website Information** | Status code, response time, server, title, cookies, redirect chain, security header quick-check |
| 2 | **HTTP Security Audit** | Audit 10 critical security headers (HSTS, CSP, X-Frame, COOP, CORP…) with a 0–100% score |
| 3 | **Technology Detection** | Detect CMS, frameworks, CDN, analytics via builtwith + header fingerprinting |
| 4 | **Metadata Crawler** | Extract all `<meta>`, Open Graph, Twitter Card, `<link>` tags, and external scripts |
| 5 | **Robots.txt & Sitemap** | Read and parse `/robots.txt`, `/sitemap.xml`, `/sitemap_index.xml` |
| 6 | **Email / Contact Harvest** | Extract emails, phone numbers, and social media links from any webpage |
| 7 | **Full Website Recon** | Combo scan: Website Info + HTTP Security Audit + Tech Detection in one pass |

### 🔗 DNS / Network
| # | Feature | Description |
|---|---------|-------------|
| 8  | **DNS Records (Full)** | Query A, AAAA, MX, NS, TXT, CNAME, SOA, SRV, CAA records |
| 9  | **Domain WHOIS** | Registrar, creation/expiry date with countdown, registrant, name servers |
| 10 | **Subdomain Enumeration** | DNS brute-force with ~100-word wordlist, 40 concurrent threads |
| 11 | **DNS Zone Transfer** | AXFR attempt against all nameservers (educational) |
| 12 | **Shared DNS Lookup** | Find domains sharing the same nameserver |
| 13 | **Forward DNS** | A, AAAA, MX, NS, TXT, CNAME, SOA lookup |

### 🖥️ IP / Host
| # | Feature | Description |
|---|---------|-------------|
| 14 | **IP Geolocation** | Country (flag emoji), region, city, ISP, AS, proxy/VPN detection, Maps link |
| 15 | **Port Scan (Threaded)** | 28 common ports, 30 threads, 1.2s timeout, banner grabbing per port |
| 16 | **Reverse IP Lookup** | Find all domains hosted on the same IP |
| 17 | **Forward IP Lookup** | Resolve domain → IPv4 (A record) |
| 18 | **Reverse DNS Lookup** | PTR record — IP → hostname |

### 🔒 SSL
| # | Feature | Description |
|---|---------|-------------|
| 19 | **SSL/TLS Certificate** | Validity dates with expiry countdown, issuer, SAN list, cipher suite, protocol |

### 📚 Extras
| # | Feature | Description |
|---|---------|-------------|
| 20 | **Tutorial / Usage Guide** | Full in-terminal guide: installation, feature reference, tips, quick examples |
| 21 | **About RYN27** | Tool info, dependencies, changelog, disclaimer, contact |

---

## 📦 Installation

### Linux & macOS
```bash
git clone https://github.com/ruyynn/RYN27.git
cd RYN27
python3 RYN27.py
```

### Windows
```bash
git clone https://github.com/ruyynn/RYN27.git
cd RYN27
python RYN27.py
```

### Termux (Android)
```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/ruyynn/RYN27.git
cd RYN27
python RYN27.py
```

### Manual (without git)
```bash
pip install requests rich python-whois dnspython builtwith beautifulsoup4 cryptography
python RYN27.py
```

> **Note:** All dependencies are installed **automatically** on first run. Manual installation is only needed if auto-install fails.

---

## 📁 Project Structure

```
RYN27/
├── RYN27.py              ← Entry point — run this
└── modules/
    ├── __init__.py       ← Package init
    ├── theme.py          ← Cross-platform color detection & Rich theme
    ├── utils.py          ← Shared helpers (clean_domain, spinner, print_result…)
    ├── logo.py           ← ASCII logo (Indonesian flag gradient) & star art
    ├── web_recon.py      ← Features 1–7  (web recon)
    ├── dns_tools.py      ← Features 8–13 (DNS & WHOIS)
    ├── ip_tools.py       ← Features 14–19 (IP, port scan, SSL)
    └── menu.py           ← Interactive menu, tutorial, about, star CTA
```

---

## 🚀 Quick Usage

```
python3 RYN27.py
```

Then pick a number from the menu:

```
[7]  Full Website Recon    →  example.com
[10] Subdomain Enumeration →  example.com
[15] Port Scan             →  192.168.1.1
[19] SSL/TLS Certificate   →  example.com
[9]  Domain WHOIS          →  example.com
[14] IP Geolocation        →  8.8.8.8
```

**Bug bounty recon workflow:**
```
[9] WHOIS → [8] DNS Records → [10] Subdomains → [7] Full Recon → [19] SSL
```

---

## ⚠️ Disclaimer

```
RYN27 is built ONLY for educational purposes and LEGAL security testing.

✅ ALLOWED on:
   - Your own servers / websites
   - Targets with explicit written permission from the owner
   - Lab environments, CTF challenges, and official bug bounty platforms

❌ PROHIBITED on:
   - Other people's websites / servers without permission
   - Government and military infrastructure
   - Public or commercial services without consent

The user is solely responsible for how this tool is used.
The developer holds no liability for any misuse or damage caused.
Violations may result in legal consequences under applicable cybercrime laws.
```

---

## 🤝 Contributing

RYN27 is an open source project that grows through community contributions. All forms of contribution are welcome.

**How to contribute:**

1. Fork this repository
2. Create a new branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin new-feature`
5. Open a Pull Request

**Or simply:**

- 🐛 [Report a bug](https://github.com/ruyynn/RYN27/issues/new?template=bug_report.md)
- 💡 [Request a feature](https://github.com/ruyynn/RYN27/issues/new?template=feature_request.md)
- ⭐ Drop a star if this tool helped you — it means a lot

[![Contributors](https://img.shields.io/github/contributors/ruyynn/RYN27?style=flat-square&color=blue)](https://github.com/ruyynn/RYN27/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/ruyynn/RYN27?style=flat-square&color=orange)](https://github.com/ruyynn/RYN27/network/members)
[![Pull Requests](https://img.shields.io/github/issues-pr/ruyynn/RYN27?style=flat-square&color=green)](https://github.com/ruyynn/RYN27/pulls)

---

## 📜 Changelog

### v1.8.0
- **Modular architecture** — split into `modules/` for maintainability
- **7 new features**: HTTP Security Audit, Subdomain Enumeration, SSL/TLS Inspector, Robots & Sitemap, Email Harvester, Full Website Recon combo, Forward DNS (full)
- **Port scan upgraded** — threaded (30 workers), banner grabbing, 28 ports
- **IP geolocation upgraded** — proxy/VPN detection, flag emoji, Maps link
- **WHOIS upgraded** — expiry countdown, updated/created date
- **In-terminal Tutorial, About page, and ⭐ Star CTA** added
- Cross-platform color detection improved (truecolor / 256 / basic / none)

### v1.0.0
- Initial release — WHOIS, DNS, IP geolocation, port scan, tech detection, reverse/forward IP & DNS, zone transfer, metadata crawler

---

## 📬 Contact

Got questions, ideas, collaboration offers, or just want to talk security? Reach out:

[![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://web.facebook.com/profile.php?id=61587795784907)
[![Gmail](https://img.shields.io/badge/-Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ruyynn25@gmail.com)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ruyynn)

---

## ☕ Donate

If RYN27 has ever helped your work or learning, consider supporting its development:

<a href="https://saweria.co/Ruyynn">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="110"/>
</a>

> Every bit of support, no matter how small, means a lot and keeps this project moving forward. Thank you! 🙏

---

*Coded with ❤️ by [Ruyynn](https://github.com/ruyynn) — from Indonesia 🇮🇩 for the global cybersecurity community*
