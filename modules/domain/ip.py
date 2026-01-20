import socket
import ipaddress
import requests


IPINFO_URL = "https://ipinfo.io/{ip}/json"
TIMEOUT = 5


def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def get_ip_info(ip: str) -> dict:
    try:
        response = requests.get(IPINFO_URL.format(ip=ip), timeout=TIMEOUT)
        if response.status_code != 200:
            return {}
        return response.json()
    except Exception:
        return {}


def reverse_dns_lookup(ip: str):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.gaierror, socket.herror):
        return None


def get_asn(ip: str):
    info = get_ip_info(ip)
    return info.get("org", None)


def get_geolocation(ip: str) -> dict:
    info = get_ip_info(ip)

    return {
        "city": info.get("city"),
        "region": info.get("region"),
        "country": info.get("country"),
        "location": info.get("loc")
    }


def analyze_ip(ip: str) -> dict:
    if not is_valid_ip(ip):
        return {
            "valid": False,
            "error": "Invalid IP address"
        }

    return {
        "valid": True,
        "ip": ip,
        "reverse_dns": reverse_dns_lookup(ip),
        "asn": get_asn(ip),
        "geolocation": get_geolocation(ip),
        "raw": get_ip_info(ip)
    }