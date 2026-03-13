# RYN27 — Ultimate Information Gathering Tool

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/Version-1.0.0-CE1126?style=for-the-badge&logo=git&logoColor=white)](https://github.com/ruyynn/RYN27/releases)
[![License](https://img.shields.io/badge/License-MIT-2ecc71?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ruyynn/RYN27?style=for-the-badge&logo=github&logoColor=white&color=f1c40f)](https://github.com/ruyynn/RYN27/stargazers)
[![Issues](https://img.shields.io/github/issues/ruyynn/RYN27?style=for-the-badge&logo=githubactions&logoColor=white&color=e74c3c)](https://github.com/ruyynn/RYN27/issues)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-555?style=for-the-badge&logo=linux&logoColor=white)]()

> **RYN27** is a CLI-based information gathering tool that combines WHOIS, DNS, port scanning, IP geolocation, reverse lookup, and technology detection into a single clean and premium terminal interface. Built for security researchers, bug bounty hunters, CTF players, and sysadmins who need a fast, lightweight, no-nonsense recon tool.

---

## 📸 Screenshot

<p>
  <img src="assets/demo.svg" width="60%"/>
  <img src="assets/preview.png" width="60%"/>
</p>

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Website Information** | Full HTTP headers, status code, response time, cookies, server, page title |
| 2 | **Domain Whois Lookup** | Registrar, creation/expiry date, name servers, email, organization, country |
| 3 | **Find IP Location** | IP geolocation — country, city, ZIP, GPS coordinates, ISP, org, AS number |
| 4 | **Port Scan** | TCP connect scan on 21 common ports with service name detection |
| 5 | **DNS Whois Lookup** | WHOIS lookup via DNS records |
| 7 | **DNS Zone Transfer** | AXFR attempt against all nameservers for DNS enumeration |
| 8 | **Reverse IP Lookup** | Find other domains hosted on the same IP |
| 9 | **Forward IP Lookup** | Resolve domain to IP address (A record) |
| 10 | **Reverse DNS Lookup** | PTR record lookup from IP to hostname |
| 11 | **Forward DNS Lookup** | A record lookup from domain |
| 12 | **Shared DNS Lookup** | Find domains sharing the same nameserver |
| 13 | **Technology Lookup** | Detect CMS, frameworks, CDN, analytics, and tech stack |
| 14 | **Website Recon** | Website information + technology lookup in one scan |
| 15 | **Metadata Crawler** | Extract all meta tags (name, property, http-equiv) from a page |

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
pip install requests rich python-whois dnspython builtwith beautifulsoup4
python RYN27.py
```

> **Note:** All dependencies are installed **automatically** on first run. Manual installation is only needed if something goes wrong.

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

## 📬 Contact

Got questions, ideas, collaboration offers, or just want to talk security? Reach out:

[![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://web.facebook.com/profile.php?id=61587795784907)
[![Gmail](https://img.shields.io/badge/-Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ruyynn25@gmail.com)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ruyynn)

---

## ☕ Donate

If RYN27 has ever helped your work or learning, consider supporting its development:

<a href="https://saweria.co/Ruyynn">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="180"/>
</a>

> Every bit of support, no matter how small, means a lot and keeps this project moving forward. Thank you! 🙏

---

*Coded with ❤️ by [RYN27](https://github.com/ruyynn) — from Indonesia 🇮🇩 for the global cybersecurity community*
