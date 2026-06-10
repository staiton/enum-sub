import dns.resolver

def dns_enum(domain):
    print(f"\n[+] Enumerating DNS for {domain}")
    print("-" * 30)

    try:
        answers = dns.resolver.resolve(domain, "A")

        print("A Records:")
        for rdata in answers:
            print(f" - {rdata}")

    except Exception as e:
        print(f"[-] Error: {e}")
