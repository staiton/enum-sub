import dns.resolver
import dns.exception


def resolve_subdomain(subdomain: str, timeout: float = 3.0) -> tuple[str, str] | None:
    """
    Resolve um subdomínio para registro A.

    Args:
        subdomain: O subdomínio completo (ex: www.example.com)
        timeout: Tempo máximo de espera em segundos

    Returns:
        Tupla (subdomain, ip) se resolver com sucesso.
        None se não resolver ou se o registro não existir.
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        resolver.lifetime = timeout

        answers = resolver.resolve(subdomain, "A")
        for rdata in answers:
            return subdomain, rdata.to_text()

    except dns.resolver.NXDOMAIN:
        # Subdomínio não existe
        return None

    except dns.resolver.NoAnswer:
        # Domínio existe mas não tem registro A
        return None

    except dns.resolver.NoNameservers:
        # Nenhum servidor DNS pôde responder
        return None

    except dns.resolver.Timeout:
        # Timeout na consulta
        return None

    except dns.exception.DNSException:
        # Qualquer outro erro de DNS
        return None


def resolve_multiple_types(subdomain: str, record_types: list[str] = None, timeout: float = 3.0) -> dict[str, list[str]] | None:
    """
    Resolve múltiplos tipos de registro para um subdomínio.

    Args:
        subdomain: O subdomínio completo
        record_types: Lista de tipos de registro (default: ["A", "AAAA", "CNAME", "MX"])
        timeout: Tempo máximo de espera por consulta

    Returns:
        Dicionário {tipo: [valores]} se houver pelo menos uma resposta.
        None se nenhuma consulta retornar resultado.
    """
    if record_types is None:
        record_types = ["A", "AAAA", "CNAME", "MX"]

    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout

    results = {}

    for rtype in record_types:
        try:
            answers = resolver.resolve(subdomain, rtype)
            results[rtype] = [rdata.to_text() for rdata in answers]
        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers,
            dns.resolver.Timeout,
            dns.exception.DNSException,
        ):
            continue

    if results:
        return results
    return None
