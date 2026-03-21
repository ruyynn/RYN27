<div align="center">

<!-- Typing SVG — Tool Name -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=36&duration=3000&pause=1500&color=CE1126&center=true&vCenter=true&width=700&height=80&lines=RYN27" alt="RYN27"/>

<!-- Typing SVG — Tagline cycling -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=2500&pause=1200&color=FFFFFF&center=true&vCenter=true&multiline=false&width=700&height=50&lines=Ultimate+Information+Gathering+Tool;WHOIS+%C2%B7+DNS+%C2%B7+Port+Scan+%C2%B7+IP+Geolocation;SSL+Inspection+%C2%B7+Tech+Detection+%C2%B7+Web+Recon;Subdomain+Enum+%C2%B7+Security+Audit+%C2%B7+Email+Harvest;One+tool.+Every+recon+you+need.+%F0%9F%87%AE%F0%9F%87%A9" alt="Tagline"/>

<!-- Typing SVG — Follow CTA -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=15&duration=2000&pause=3000&color=FFD700&center=true&vCenter=true&width=700&height=40&lines=%E2%98%85+Follow+%40ruyynn+on+GitHub+%E2%80%94+github.com%2Fruyynn+%E2%98%85" alt="Follow Ruyynn"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/Version-1.8.0-CE1126?style=for-the-badge&logo=git&logoColor=white)](https://github.com/ruyynn/RYN27/releases)
[![License](https://img.shields.io/badge/License-MIT-2ecc71?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ruyynn/RYN27?style=for-the-badge&logo=github&logoColor=white&color=f1c40f)](https://github.com/ruyynn/RYN27/stargazers)
[![Issues](https://img.shields.io/github/issues/ruyynn/RYN27?style=for-the-badge&logo=githubactions&logoColor=white&color=e74c3c)](https://github.com/ruyynn/RYN27/issues)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-555?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/ruyynn/RYN27)

<br/>

**Built for** `bug bounty hunters` · `CTF players` · `pentesters` · `security researchers`

<br/>

</div>

---
 
## ◈ &nbsp; About
 
**RYN27** is a free, open-source CLI tool for **OSINT and information gathering**, built with a premium terminal UI powered by [Rich](https://github.com/Textualize/rich). It bundles 19 recon modules into a single interactive menu — no config files, no API keys required for most features, no bloat.
 
The tool was designed to be **fast to launch and easy to use** — type a domain or IP, pick a number, get results. Everything from WHOIS to SSL certificate inspection to threaded port scanning runs from the same interface, with clean formatted output that's easy to read and share.
 
| | |
|---|---|
| **Language** | Python 3.9+ |
| **Architecture** | Modular — `modules/` structure, easy to extend |
| **UI** | [Rich](https://github.com/Textualize/rich) — panels, tables, progress bars, truecolor themes |
| **Platform** | Linux · macOS · Windows · Android (Termux) |
| **Dependencies** | Auto-installed on first run |
| **License** | MIT |
 
---

<div align="center">

## ✦ &nbsp; PREVIEW &nbsp; ✦

<img src="assets/demo.svg" width="80%"/>
<br/><br/>
<img src="assets/preview.png" width="80%"/>

</div>

---

<div align="center">

## ✦ &nbsp; GIVE IT A STAR &nbsp; ✦

**If RYN27 has ever helped your recon, your bounty, or your learning —**
**a ⭐ star is the best way to say thank you.**

[![Star RYN27 on GitHub](https://img.shields.io/badge/⭐%20Star%20RYN27%20on%20GitHub-FFD700?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ruyynn/RYN27)

*It takes 2 seconds. It means everything. 🙏*

</div>

---

## ◈ &nbsp; Features

<details open>
<summary><b>🌐 Web Recon</b></summary>
<br/>

| # | Feature | What You Get |
|:---:|---------|-------------|
| `01` | **Website Information** | Status code, response time, server fingerprint, page title, cookies, redirect chain, security header snapshot |
| `02` | **HTTP Security Audit** | Deep audit of 10 critical headers — HSTS, CSP, X-Frame-Options, COOP, CORP, COEP — with a visual **0–100% security score** |
| `03` | **Technology Detection** | Full stack fingerprint via builtwith + header analysis — CMS, framework, CDN, analytics, caching layer |
| `04` | **Metadata Crawler** | All `<meta>` tags, Open Graph (`og:`), Twitter Card, `<link>` tags, and external script inventory |
| `05` | **Robots & Sitemap** | Reads and parses `/robots.txt`, `/sitemap.xml`, `/sitemap_index.xml` |
| `06` | **Email / Contact Harvest** | Extracts email addresses, phone numbers, and social media links (FB, IG, LinkedIn, GitHub, Telegram…) |
| `07` | **Full Website Recon** | **Combo:** Website Info + HTTP Audit + Tech Detection — complete first-look recon in one pass |

</details>

<details open>
<summary><b>🔗 DNS / Network</b></summary>
<br/>

| # | Feature | What You Get |
|:---:|---------|-------------|
| `08` | **DNS Records (Full)** | A, AAAA, MX, NS, TXT, CNAME, SOA, SRV, CAA — every record type in one query |
| `09` | **Domain WHOIS** | Registrar, creation & expiry dates with **live countdown**, registrant org/country, name servers |
| `10` | **Subdomain Enumeration** | DNS brute-force with ~100 curated wordlist, **40 concurrent threads** — fast and dependency-free |
| `11` | **DNS Zone Transfer** | AXFR attempt against all nameservers — catches misconfigured DNS servers |
| `12` | **Shared DNS Lookup** | Discover domains sharing the same nameserver via HackerTarget API |
| `13` | **Forward DNS** | A, AAAA, MX, NS, TXT, CNAME, SOA lookup |

</details>

<details open>
<summary><b>🖥️ IP / Host</b></summary>
<br/>

| # | Feature | What You Get |
|:---:|---------|-------------|
| `14` | **IP Geolocation** | Country (flag 🏳️), region, city, ISP, AS number, **proxy/VPN detection**, Google Maps link |
| `15` | **Port Scan (Threaded)** | 28 common ports · **30 worker threads** · 1.2s timeout · HTTP **banner grabbing** per open port |
| `16` | **Reverse IP Lookup** | All domains co-hosted on the same IP address |
| `17` | **Forward IP Lookup** | Domain → IPv4 (A record) resolution |
| `18` | **Reverse DNS Lookup** | PTR record — IP address → hostname |

</details>

<details open>
<summary><b>🔒 SSL / TLS</b></summary>
<br/>

| # | Feature | What You Get |
|:---:|---------|-------------|
| `19` | **SSL/TLS Certificate** | Validity dates with **expiry countdown**, issuer chain, Subject Alt Names, cipher suite, protocol version |

</details>

<details>
<summary><b>📚 Built-in Extras</b></summary>
<br/>

| # | Feature | What You Get |
|:---:|---------|-------------|
| `20` | **Tutorial / Usage Guide** | Full in-terminal guide — installation, feature reference, tips & best practices, real-world examples |
| `21` | **About RYN27** | Tool info, dependencies, changelog, disclaimer, contact & donate links |
</details>

---

## ◈ &nbsp; Installation

<details open>
<summary><b>Linux / macOS</b></summary>

```bash
git clone https://github.com/ruyynn/RYN27.git
cd RYN27
python3 RYN27.py
```

</details>

<details>
<summary><b>Windows</b></summary>

```bash
git clone https://github.com/ruyynn/RYN27.git
cd RYN27
python RYN27.py
```

</details>

<details>
<summary><b>Termux (Android)</b></summary>

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/ruyynn/RYN27.git
cd RYN27
python RYN27.py
```

</details>

<details>
<summary><b>Manual pip install</b></summary>

```bash
pip install requests rich python-whois dnspython builtwith beautifulsoup4 cryptography
python RYN27.py
```

</details>

> **All dependencies install automatically on first run.** Manual install is only needed if auto-install fails.

---

## ◈ &nbsp; Quick Start

```bash
python3 RYN27.py
```

Pick a number and go:

```
[7]   Full Website Recon      →  example.com
[10]  Subdomain Enumeration   →  example.com
[15]  Port Scan               →  192.168.1.1  or  example.com
[19]  SSL/TLS Certificate     →  example.com
[9]   Domain WHOIS            →  example.com
[14]  IP Geolocation          →  8.8.8.8
[2]   HTTP Security Audit     →  example.com
[6]   Email Harvest           →  example.com
```

**Recommended bug bounty recon chain:**

```
[9] WHOIS  →  [8] DNS Records  →  [10] Subdomains  →  [7] Full Recon  →  [19] SSL  →  [2] Security Audit
```

---

## ◈ &nbsp; Project Structure

```
RYN27/
│
├── RYN27.py                ← Entry point — run this
│
└── modules/
    ├── __init__.py         ← Package init
    ├── theme.py            ← Cross-platform color detection & Rich theme engine
    ├── utils.py            ← Shared helpers — clean_domain, spinner, print_result…
    ├── logo.py             ← ASCII logo (Indonesian flag gradient 🇮🇩) + star art
    ├── web_recon.py        ← Features  1–7   (web recon)
    ├── dns_tools.py        ← Features  8–13  (DNS & WHOIS)
    ├── ip_tools.py         ← Features 14–19  (IP, port scan, SSL)
    └── menu.py             ← Menu · Tutorial · About
```

---

## ◈ &nbsp; Disclaimer

```
RYN27 is built ONLY for educational purposes and LEGAL security testing.

✅ ALLOWED:
   • Your own servers and websites
   • Targets with explicit written permission from the owner
   • Lab environments, CTF challenges, official bug bounty platforms

❌ PROHIBITED:
   • Other people's servers / websites without permission
   • Government and military infrastructure
   • Any public or commercial service without consent

The user is solely responsible for how this tool is used.
The developer holds no liability for any misuse or damage caused.
Violations may result in legal consequences under applicable cybercrime laws.
```

---

## ◈ &nbsp; Changelog

<details open>
<summary><b>v1.8.0 — Current</b></summary>

- 🏗️ **Modular architecture** — clean `modules/` structure, easy to extend
- ✨ **7 new features** — HTTP Security Audit, Subdomain Enum, SSL/TLS Inspector, Robots & Sitemap, Email Harvester, Full Website Recon, Forward DNS (full)
- ⚡ **Port scan** — threaded (30 workers), banner grabbing, 28 ports (was 21)
- 🌍 **IP Geolocation** — proxy/VPN detection, flag emoji, Google Maps link
- 📋 **WHOIS** — expiry countdown (expired / expiring soon / safe), updated date
- 📖 **In-terminal Tutorial, About page** added as menu options
- 🎨 **Improved color support** — truecolor / 256 / basic / none degradation

</details>

<details>
<summary><b>v1.0.0 — Initial Release</b></summary>

- First release — WHOIS, DNS, IP geolocation, port scan, tech detection, reverse/forward IP & DNS, zone transfer, metadata crawler

</details>

---

## ◈ &nbsp; Contributing

RYN27 grows through community contributions. All forms are welcome.

```bash
# 1. Fork the repo
# 2. Create your branch
git checkout -b feature/amazing-feature

# 3. Commit your changes
git commit -m "Add amazing feature"

# 4. Push and open a PR
git push origin feature/amazing-feature
```

Or simply:
- 🐛 [Report a bug](https://github.com/ruyynn/RYN27/issues/new?template=bug_report.md)
- 💡 [Request a feature](https://github.com/ruyynn/RYN27/issues/new?template=feature_request.md)
- ⭐ [Drop a star](https://github.com/ruyynn/RYN27) — it genuinely helps

<br/>

[![Contributors](https://img.shields.io/github/contributors/ruyynn/RYN27?style=flat-square&color=blue)](https://github.com/ruyynn/RYN27/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/ruyynn/RYN27?style=flat-square&color=orange)](https://github.com/ruyynn/RYN27/network/members)
[![Pull Requests](https://img.shields.io/github/issues-pr/ruyynn/RYN27?style=flat-square&color=green)](https://github.com/ruyynn/RYN27/pulls)

---

## ◈ &nbsp; Contact

Got questions, ideas, or just want to talk security?

<br/>

[![Follow on GitHub](https://img.shields.io/badge/Follow-%40ruyynn-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ruyynn)
[![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://web.facebook.com/profile.php?id=61587795784907)
[![Gmail](https://img.shields.io/badge/-Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ruyynn25@gmail.com)

---

## ◈ &nbsp; Support the Project

<div align="center">

If RYN27 has helped your work or learning, consider buying me a coffee.
Every bit of support keeps this free and maintained. 🙏

<br/>

<a href="https://saweria.co/Ruyynn">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="150"/>
</a>

</div>

---

<div align="center">

<!-- Footer typing SVG -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=14&duration=3000&pause=2000&color=6C7A89&center=true&vCenter=true&width=700&height=40&lines=Coded+with+%E2%9D%A4%EF%B8%8F+by+Ruyynn+%E2%80%94+from+Indonesia+%F0%9F%87%AE%F0%9F%87%A9+for+the+global+cybersecurity+community" alt="Footer"/>

<br/>

## Star History

<a href="https://www.star-history.com/?repos=ruyynn%2FRYN27&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=ruyynn/RYN27&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=ruyynn/RYN27&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=ruyynn/RYN27&type=date&legend=top-left" />
  
 </picture>

</a>

</div>
 
