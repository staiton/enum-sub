# enum-sub

A simple Python-based subdomain enumeration tool using DNS resolution and wordlist brute force techniques.

> This tool is intended for educational purposes and authorized security testing only.

---

## Features

- DNS resolution (A records)
- Subdomain brute force using wordlists
- Real-time scanning output in terminal
- Lightweight and easy to extend
- Modular Python structure

---

## Project Structure

enum-sub/
├── enum_sub/
│ ├── init.py
│ ├── main.py
│ └── dns_enum.py
│
├── wordlist.txt
├── requirements.txt
├── README.md
└── .venv/

---

## Requirements

- Python 3.8+
- Linux (tested on Pop!_OS)
- dnspython

Install dependencies:

```bash
pip install -r requirements.txt

---

## Installation

git clone https://github.com/your-username/enum-sub.git
cd enum-sub
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

---

## Usage

python3 -m enum_sub.main example.com -w wordlist.txt

---

## Example Output

[+] Starting subdomain brute force on example.com
--------------------------------------------------
[TESTING] www.example.com
[TESTING] mail.example.com
[FOUND] api.example.com -> 93.184.216.34
[TESTING] ftp.example.com

[+] Finished.

---

## How it works

1. Loads a wordlist of common subdomain names
2. Appends each word to the target domain
3. Performs DNS A record lookup
4. Displays results in real-time

---

## Legal Disclaimer

This tool is for:

Educational purposes
Authorized penetration testing
Security research in controlled environments

Do NOT use against domains you do not own or have permission to test.

The author is not responsible for misuse.

## Author

Gabriel França

Cybersecurity enthusiast • Network analyst •
