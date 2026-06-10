import argparse
from enum_sub.dns_enum import brute_force_subdomains

def main():
    parser = argparse.ArgumentParser(description="Enum-Sub Tool")
    
    parser.add_argument("domain", help="Target domain")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist", required=True)

    args = parser.parse_args()

    brute_force_subdomains(args.domain, args.wordlist)

if __name__ == "__main__":
    main()
