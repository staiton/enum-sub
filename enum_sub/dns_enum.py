import dns.resolver
import dns.exception


def resolve_subdomain(subdomain: str):
    """
    Resolve um subdomínio e retorna (subdomain, ip) se existir.
    Retorna None se não resolver.
    """
    try:
        answers = dns.resolver.resolve(subdomain, "A", lifetime=3)
        for rdata in answers:
            return subdomain, rdata.to_text()
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.Timeout,
        dns.exception.DNSException,
    ):
        return None
