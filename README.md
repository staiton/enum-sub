
# ENUM-SUB TOOL

A simple Python-based subdomain enumeration tool using DNS resolution and wordlist brute force techniques.

> This tool is intended for educational purposes and authorized security testing only.


## Features

- DNS resolution (A records)
- Subdomain brute force using wordlists
- Multithreaded subdomain brute force
- Real-time CLI status display
- Clean and stable terminal output
- Lightweight and easy to extend
- Modular Python structure

---
## Project Structure

```bash
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
```

---
## Requirements

- Python 3.8+
- Linux (tested on Pop!_OS)
- dnspython

Install dependencies:

```bash
pip install -r requirements.txt
```

---
## Installation

```bash
git clone https://github.com/staiton/enum-sub.git
cd enum-sub
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
    
## Usage

```bash
python3 -m enum_sub.main example.com -w wordlist.txt -t 20
```

---
## Example Output

```bash

╔════════════════════════════════════════════╗
║               ENUM-SUB TOOL                ║
║        Subdomain Brute Force Scanner       ║
╠════════════════════════════════════════════╣
║  Author : staiton                          ║
║  Mode   : Multithreaded DNS Enumeration    ║
║  Status : Ready                            ║
╠════════════════════════════════════════════╣
║  Use only on authorized targets            ║
╚════════════════════════════════════════════╝

[+] Starting subdomain brute force on example.com
[+] Wordlist size: 999
[+] Threads: 20
--------------------------------------------------
[TESTING] www.example.com (8/999)                                               
[FOUND] www.example.com -> 104.20.23.154
                                                                                
--------------------------------------------------
[+] Finished. 1 subdomains found.

```

---
## How it works

1. Loads a wordlist of common subdomain names
2. Appends each word to the target domain
3. Performs DNS A record lookup
4. Uses multithreading for fast DNS resolution
5. Displays live scanning status in terminal
6. Ensures clean output during concurrent execution

---
## Legal Disclaimer

This tool is for:

Educational purposes
Authorized penetration testing
Security research in controlled environments

Do NOT use against domains you do not own or have permission to test.

The author is not responsible for misuse.
## Author

- [@staiton](https://www.github.com/staiton)

