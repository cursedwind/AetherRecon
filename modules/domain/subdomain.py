import dns.resolver
import requests


CRT_URL = "https://crt.sh/?q=%25.{domain}&output=json"
TIMEOUT = 8


def resolve_subdomain(subdomain: str):
    try:
        answers = dns.resolver.resolve(subdomain, "A", lifetime=TIMEOUT)
        return [str(r.address) for r in answers]
    except Exception:
        return []


def from_crtsh(domain: str) -> list:
    subdomains = set()

    try:
        response = requests.get(CRT_URL.format(domain=domain), timeout=TIMEOUT)
        if response.status_code != 200:
            return []

        data = response.json()

        for entry in data:
            name_value = entry.get("name_value", "")
            for sub in name_value.split("\n"):
                if "*" not in sub and sub.endswith(domain):
                    subdomains.add(sub.strip())

    except Exception:
        pass

    return sorted(subdomains)


def bruteforce(domain: str, wordlist: list) -> list:
    found = set()

    for word in wordlist:
        sub = f"{word.strip()}.{domain}"
        ips = resolve_subdomain(sub)
        if ips:
            found.add(sub)

    return sorted(found)


def enumerate_subdomains(domain: str, wordlist: list = None) -> dict:
    results = set()

    results |= set(from_crtsh(domain))

    if wordlist:
        results |= set(bruteforce(domain, wordlist))

    resolved = {}

    for sub in results:
        ips = resolve_subdomain(sub)
        if ips:
            resolved[sub] = ips

    return {
        "domain": domain,
        "total_found": len(results),
        "subdomains": sorted(results),
        "resolved": resolved
    }
