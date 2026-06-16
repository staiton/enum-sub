import argparse
import sys
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from enum_sub.dns_enum import resolve_subdomain

print_lock = threading.Lock()
found_lock = threading.Lock()


def print_banner():
    banner = """
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
"""
    safe_print(banner)


def safe_print(text: str = ""):
    """Imprime com lock para evitar output embaralhado."""
    with print_lock:
        print(text)


def print_status(text: str):
    """Atualiza uma única linha no terminal."""
    with print_lock:
        sys.stdout.write("\r" + " " * 80)
        sys.stdout.write("\r" + text)
        sys.stdout.flush()


def load_wordlist(path: str) -> list[str]:
    """Carrega a wordlist do arquivo, uma sub por linha."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        safe_print(f"[!] Wordlist not found: {path}")
        sys.exit(1)
    except PermissionError:
        safe_print(f"[!] Permission denied: {path}")
        sys.exit(1)


def check_wildcard(domain: str) -> str | None:
    """
    Detecta wildcard DNS gerando um subdomínio aleatório.
    Retorna o IP do wildcard ou None se não houver.
    """
    random_label = uuid.uuid4().hex[:12]
    random_sub = f"{random_label}.{domain}"
    result = resolve_subdomain(random_sub)
    if result:
        _, ip = result
        return ip
    return None


def run_scan(domain: str, wordlist: list[str], threads: int, wildcard_ip: str | None) -> list[tuple[str, str]]:
    """Executa o scan multithreaded e retorna lista de (subdomain, ip)."""
    total = len(wordlist)
    tested = 0
    found = []

    safe_print(f"[+] Target   : {domain}")
    safe_print(f"[+] Wordlist : {total} entries")
    safe_print(f"[+] Threads  : {threads}")
    if wildcard_ip:
        safe_print(f"[!] Wildcard detected: *.{domain} -> {wildcard_ip}")
        safe_print(f"[!] Wildcard responses will be filtered out.")
    safe_print("-" * 50)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_sub = {}

        for word in wordlist:
            subdomain = f"{word}.{domain}"
            future = executor.submit(resolve_subdomain, subdomain)
            future_to_sub[future] = subdomain

        for future in as_completed(future_to_sub):
            tested += 1
            current = future_to_sub[future]

            print_status(f"[TESTING] {current} ({tested}/{total})")

            result = future.result()
            if result:
                sub, ip = result

                # Filtra respostas de wildcard
                if wildcard_ip and ip == wildcard_ip:
                    continue

                with found_lock:
                    found.append((sub, ip))
                safe_print(f"\n[FOUND] {sub} -> {ip}")

    print_status("")
    return found


def save_results(found: list[tuple[str, str]], output_path: str):
    """Salva os resultados encontrados em arquivo CSV."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("subdomain,ip\n")
            for sub, ip in found:
                f.write(f"{sub},{ip}\n")
        safe_print(f"[+] Results saved to {output_path}")
    except PermissionError:
        safe_print(f"[!] Cannot write to {output_path} — permission denied")


def print_summary(found: list[tuple[str, str]]):
    """Imprime o resumo final dos resultados."""
    safe_print("\n" + "-" * 50)
    safe_print(f"[+] Scan complete. {len(found)} subdomain(s) found.")
    if found:
        safe_print("")
        safe_print(f" {'SUBDOMAIN':<45} {'IP'}")
        safe_print(f" {'─' * 44} {'─' * 15}")
        for sub, ip in sorted(found):
            safe_print(f" {sub:<45} {ip}")


def main():
    parser = argparse.ArgumentParser(
        description="Multithreaded subdomain brute force tool"
    )
    parser.add_argument(
        "domain",
        help="Target domain (example.com)",
    )
    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Path to wordlist file",
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=20,
        help="Number of concurrent threads (default: 20)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Save results to file (CSV format)",
    )
    parser.add_argument(
        "--no-wildcard-check",
        action="store_true",
        help="Skip wildcard DNS detection",
    )

    args = parser.parse_args()

    print_banner()

    # Carrega wordlist
    words = load_wordlist(args.wordlist)
    if not words:
        safe_print("[!] Wordlist is empty.")
        sys.exit(1)

    # Wildcard detection
    wildcard_ip = None
    if not args.no_wildcard_check:
        safe_print("[*] Checking for wildcard DNS...")
        wildcard_ip = check_wildcard(args.domain)

    try:
        # Executa o scan
        found = run_scan(args.domain, words, args.threads, wildcard_ip)

        # Salva em arquivo se solicitado
        if args.output:
            save_results(found, args.output)

        # Imprime resumo
        print_summary(found)

    except KeyboardInterrupt:
        safe_print("\n\n[!] Interrupted by user. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
