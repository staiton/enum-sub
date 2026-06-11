import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum_sub.dns_enum import resolve_subdomain

def print_banner():
    print("""
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
""")

def load_wordlist(path: str):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def print_status(text: str):
    """
    Atualiza uma única linha no terminal.
    """
    sys.stdout.write("\r" + " " * 80)
    sys.stdout.write("\r" + text)
    sys.stdout.flush()


def main(domain: str, wordlist_path: str, threads: int):
    print_banner()
    words = load_wordlist(wordlist_path)
    total = len(words)
    tested = 0

    print(f"[+] Starting subdomain brute force on {domain}")
    print(f"[+] Wordlist size: {total}")
    print(f"[+] Threads: {threads}")
    print("-" * 50)

    found = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_sub = {}

        for word in words:
            subdomain = f"{word}.{domain}"
            future = executor.submit(resolve_subdomain, subdomain)
            future_to_sub[future] = subdomain

        for future in as_completed(future_to_sub):
            tested += 1
            current = future_to_sub[future]

            # linha única de status
            print_status(f"[TESTING] {current} ({tested}/{total})")

            result = future.result()
            if result:
                sub, ip = result
                found.append(sub)
                print(f"\n[FOUND] {sub} -> {ip}")

    print_status("")  # limpa a linha
    print("\n" + "-" * 50)
    print(f"[+] Finished. {len(found)} subdomains found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multithreaded subdomain brute force tool"
    )
    parser.add_argument("domain", help="Target domain (example.com)")
    parser.add_argument(
        "-w", "--wordlist", required=True, help="Path to wordlist file"
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=20,
        help="Number of concurrent threads (default: 20)",
    )

    args = parser.parse_args()
    main(args.domain, args.wordlist, args.threads)
