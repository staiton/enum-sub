import dns.resolver
import sys

def resolve(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, "A")
        return [rdata.to_text() for rdata in answers]
    except:
        return None


def brute_force_subdomains(domain, wordlist_path):
    print(f"\n[+] Starting subdomain brute force on {domain}")
    print("-" * 50)

    with open(wordlist_path, "r") as file:
        words = file.read().splitlines()

    for word in words:
        subdomain = f"{word}.{domain}"

        sys.stdout.write(f"\r[TESTING] {subdomain}   ")
        sys.stdout.flush()

        result = resolve(subdomain)

        if result:
            print(f"\n[FOUND] {subdomain} -> {', '.join(result)}")

    print("\n\n[+] Finished.")
