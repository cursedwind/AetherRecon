import socket
import dns.resolver

def resolve_domain(domain):
    try:
        ip_addresses = socket.gethostbyname_ex(domain)[2]
        return ip_addresses
    except socket.gaierror:
        return []
    
def get_mx_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_records = [str(r.exchange) for r in answers]
        return mx_records
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def get_ns_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        ns_records = [str(r.target) for r in answers]
        return ns_records
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def get_txt_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        txt_records = [b''.join(r.strings).decode('utf-8') for r in answers]
        return txt_records
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def get_cname_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        cname_record = [str(r.target) for r in answers]
        return cname_record
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def get_aaaa_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'AAAA')
        aaaa_records = [str(r.address) for r in answers]
        return aaaa_records
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def get_a_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        a_records = [str(r.address) for r in answers]
        return a_records
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []   