# Classic Libraries
import threading
import queue
import time
import logging
import signal

# Core
from core.config import *
from core.app_logger import Logger

# Domain Modules
from modules.domain.dns import (
    resolve_domain,
    get_mx_records,
    get_ns_records,
    get_a_records,
    get_aaaa_records,
    get_cname_record,
    get_txt_records
)

from modules.domain.ip import (
    analyze_ip,
    is_valid_ip,
    get_ip_info,
    reverse_dns_lookup,
    get_asn,
    get_geolocation
)

from modules.domain.subdomain import (
    enumerate_subdomains,
    from_crtsh,
    bruteforce,
    resolve_subdomain
)

# Utils
from utils.http import analyze_http
from utils.parser import parse_json_file, parse_timestamp


class Engine:
    def __init__(self):
        self.logger = Logger("AetherRecon").logger

        self.stop_event = threading.Event()

        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        self.logger.info("Engine initialized successfully.")


    def handle_shutdown(self, signum, frame):
        self.logger.info("Shutdown signal received. Stopping engine...")
        self.stop_event.set()

    def shutdown(self):
        self.logger.info("Shutting down engine...")
        self.stop_event.set()

    def wait_for_shutdown(self):
        while not self.stop_event.is_set():
            time.sleep(1)
        self.logger.info("Engine has been stopped cleanly.")


    def run_domain_analysis(self, domain: str) -> dict:
        self.logger.info(f"Running full domain analysis for {domain}...")

        result = {
            "domain": domain,
            "dns": {
                "a_records": get_a_records(domain),
                "aaaa_records": get_aaaa_records(domain),
                "mx_records": get_mx_records(domain),
                "ns_records": get_ns_records(domain),
                "cname_record": get_cname_record(domain),
                "txt_records": get_txt_records(domain)
            },
        }

        self.logger.info(f"Domain analysis completed for {domain}.")
        return result

    def resolve_domain(self, domain: str):
        self.logger.info(f"Resolving domain {domain}...")
        return resolve_domain(domain)


    def subdomain_enumeration(self, domain: str):
        self.logger.info(f"Enumerating subdomains for {domain}...")
        return enumerate_subdomains(domain)

    def subdomain_bruteforce(self, domain: str, wordlist: str):
        self.logger.info(f"Bruteforcing subdomains for {domain} with {wordlist}...")
        return bruteforce(domain, wordlist)

    def resolve_subdomain(self, subdomain: str):
        self.logger.info(f"Resolving subdomain {subdomain}...")
        return resolve_subdomain(subdomain)

    def from_crtsh(self, domain: str):
        self.logger.info(f"Fetching subdomains from crt.sh for {domain}...")
        return from_crtsh(domain)
    
    def run_subdomain(self, domain: str):
        self.logger.info(f"Running full subdomain enumeration for {domain}...")
        result = enumerate_subdomains(domain)
        return result


    def run_ip_analysis(self, ip: str):
        self.logger.info(f"Running full IP analysis for {ip}...")
        return analyze_ip(ip)

    def check_ip(self, ip: str):
        self.logger.info(f"Checking if {ip} is a valid IP...")
        return is_valid_ip(ip)

    def get_ip_info(self, ip: str):
        self.logger.info(f"Getting IP info for {ip}...")
        return get_ip_info(ip)

    def reverse_dns_lookup(self, ip: str):
        self.logger.info(f"Performing reverse DNS lookup for {ip}...")
        return reverse_dns_lookup(ip)

    def get_asn(self, ip: str):
        self.logger.info(f"Getting ASN for {ip}...")
        return get_asn(ip)

    def get_geolocation(self, ip: str):
        self.logger.info(f"Getting geolocation for {ip}...")
        return get_geolocation(ip)


    def analyze_http(self, domain: str):
        self.logger.info(f"Analyzing HTTP for {domain}...")
        result = analyze_http(domain)
        self.logger.info(f"HTTP analysis completed for {domain}.")
        return result
