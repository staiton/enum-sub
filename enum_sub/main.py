import argparse
from enum_sub.dns_enum import dns_enum

def main():
    parser = argparse.ArgumentParser(description="Enum-Sub Tool")
    parser.add_argument("domain", help="Target domain")

    args = parser.parse_args()

    dns_enum(args.domain)

if __name__ == "__main__":
    main()
