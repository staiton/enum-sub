import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum_sub.dns_enum import resolve_subdomain


def load_wordlist(path: str):
    """
    Carrega a wordlist e remove linhas vazias.
    """
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def main(domain: str, wordlist_path: str, threads: int):
    words = load_wordlist(wordlist_path)

    print(f"[+] Starting subdomain brute force on {domain}")
    print(f"[+] Wordlist size: {len(words)}")
    print(f"[+] Threads: {threads}")
    print("-" * 50)

    found = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {}

        for word in words:
            subdomain = f"{word}.{domain}"
            future = executor.submit(resolve_subdomain, subdomain)
            futures[future] = subdomain

            # output em tempo real (subdomínio atual)
            sys.stdout.write(f"\r[TESTING] {subdomain} ")
            sys.stdout.flush()

        for future in as_completed(futures):
            result = future.result()
            if result:
                sub, ip = result
                found.append(sub)
                print(f"\n[FOUND] {sub} -> {ip}")

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
