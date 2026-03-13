# RYN27 — Ultimate Information Gathering Tool
 
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Version](https://img.shields.io/badge/Version-1.0.0-CE1126?style=for-the-badge&logo=git&logoColor=white)](https://github.com/ruyynn/RYN27/releases)
[![License](https://img.shields.io/badge/License-MIT-2ecc71?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ruyynn/RYN27?style=for-the-badge&logo=github&logoColor=white&color=f1c40f)](https://github.com/ruyynn/RYN27/stargazers)
[![Issues](https://img.shields.io/github/issues/ruyynn/RYN27?style=for-the-badge&logo=githubactions&logoColor=white&color=e74c3c)](https://github.com/ruyynn/RYN27/issues)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-555?style=for-the-badge&logo=linux&logoColor=white)]()
 
> **RYN27** adalah alat *information gathering* berbasis CLI yang menggabungkan WHOIS, DNS, port scanning, IP geolocation, reverse lookup, dan technology detection dalam satu antarmuka terminal yang bersih dan premium. Dibuat untuk security researcher, bug bounty hunter, CTF player, dan sysadmin yang butuh tool recon yang cepat, ringan, dan tidak ribet.
 
---
 
## 📸 Screenshot
 
![RYN27 Preview](assets/preview.png)
 
---

## ✨ Fitur

| # | Fitur | Deskripsi |
|---|-------|-----------|
| 1 | **Website Information** | HTTP headers lengkap, status code, response time, cookies, server, page title |
| 2 | **Domain Whois Lookup** | Registrar, creation/expiry date, name servers, email, organisasi, negara |
| 3 | **Find IP Location** | Geolocation IP — negara, kota, ZIP, koordinat GPS, ISP, org, AS number |
| 4 | **Port Scan** | TCP connect scan ke 21 port umum dengan deteksi nama service |
| 5 | **DNS Whois Lookup** | WHOIS lookup via DNS records |
| 7 | **DNS Zone Transfer** | AXFR attempt ke seluruh nameserver untuk enumerasi DNS |
| 8 | **Reverse IP Lookup** | Temukan domain lain yang hosted di IP yang sama |
| 9 | **Forward IP Lookup** | Resolve domain ke IP address (A record) |
| 10 | **Reverse DNS Lookup** | PTR record lookup dari IP ke hostname |
| 11 | **Forward DNS Lookup** | A record lookup dari domain |
| 12 | **Shared DNS Lookup** | Temukan domain yang berbagi nameserver yang sama |
| 13 | **Technology Lookup** | Deteksi CMS, framework, CDN, analytics, dan stack teknologi lainnya |
| 14 | **Website Recon** | Gabungan website information + technology lookup dalam satu scan |
| 15 | **Metadata Crawler** | Ekstrak semua meta tags (name, property, http-equiv) dari halaman |

---

## 📦 Instalasi

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

### Manual (tanpa git)
```bash
pip install requests rich python-whois dnspython builtwith beautifulsoup4
python RYN27.py
```

> **Note:** Semua dependencies terinstall **otomatis** saat pertama kali dijalankan. Tidak perlu install manual kecuali ada masalah.

---

## ⚠️ Disclaimer

```
RYN27 dibuat HANYA untuk keperluan edukasi dan pengujian keamanan yang LEGAL.

✅ BOLEH digunakan pada:
   - Server / website milik sendiri
   - Target dengan izin tertulis eksplisit dari pemilik
   - Lab environment, CTF, dan platform bug bounty resmi

❌ DILARANG digunakan pada:
   - Website / server orang lain tanpa izin
   - Infrastruktur pemerintah dan militer
   - Layanan publik dan komersial tanpa persetujuan

Penggunaan tool ini sepenuhnya menjadi tanggung jawab pengguna.
Developer tidak bertanggung jawab atas segala bentuk penyalahgunaan.
Pelanggaran dapat dikenakan sanksi hukum sesuai UU ITE dan regulasi setempat.
```

---

## 🤝 Kontribusi

RYN27 adalah proyek open source dan berkembang berkat kontribusi komunitas. Semua bentuk kontribusi diterima dengan tangan terbuka.

**Cara berkontribusi:**

1. Fork repository ini
2. Buat branch baru: `git checkout -b fitur-baru`
3. Commit perubahan: `git commit -m "Tambah fitur baru"`
4. Push ke branch: `git push origin fitur-baru`
5. Buat Pull Request

**Atau cukup:**

- 🐛 [Laporkan bug](https://github.com/ruyynn/RYN27/issues/new?template=bug_report.md)
- 💡 [Usulkan fitur](https://github.com/ruyynn/RYN27/issues/new?template=feature_request.md)
- ⭐ Beri bintang kalau tool ini bermanfaat — itu sudah sangat berarti

[![Contributors](https://img.shields.io/github/contributors/ruyynn/RYN27?style=flat-square&color=blue)](https://github.com/ruyynn/RYN27/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/ruyynn/RYN27?style=flat-square&color=orange)](https://github.com/ruyynn/RYN27/network/members)
[![Pull Requests](https://img.shields.io/github/issues-pr/ruyynn/RYN27?style=flat-square&color=green)](https://github.com/ruyynn/RYN27/pulls)

---

## 📬 Kontak

Ada pertanyaan, ide, kolaborasi, atau sekadar mau ngobrol soal security? Reach out:

[![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://web.facebook.com/profile.php?id=61587795784907)
[![Gmail](https://img.shields.io/badge/-Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ruyynn25@gmail.com)
[![GitHub](https://img.shields.io/badge/-Github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ruyynn)

---

## ☕ Donasi

Kalau RYN27 pernah ngebantu pekerjaan atau belajarmu, consider untuk support pengembangan lebih lanjut:

<a href="https://saweria.co/Ruyynn">
  <img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="180"/>
</a>

> Setiap dukungan sekecil apapun sangat berarti dan membantu tool ini terus berkembang. Terima kasih! 🙏

---

*Coded with ❤️ by [RYN27](https://github.com/ruyynn) — dari Indonesia 🇮🇩 untuk komunitas keamanan siber dunia*
