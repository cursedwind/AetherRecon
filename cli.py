import argparse
import sys
import json

from core.engine import Engine
from core.config import APP_NAME, APP_VERSION


def banner():
    print(f"""                                                                                                                        
    ▄▄                         ▄▄                            ▄▄▄▄▄▄                                                     
   ████                ██      ██                            ██▀▀▀▀██                                                   
   ████     ▄████▄   ███████   ██▄████▄   ▄████▄    ██▄████  ██    ██   ▄████▄    ▄█████▄   ▄████▄   ██▄████▄           
  ██  ██   ██▄▄▄▄██    ██      ██▀   ██  ██▄▄▄▄██   ██▀      ███████   ██▄▄▄▄██  ██▀    ▀  ██▀  ▀██  ██▀   ██           
  ██████   ██▀▀▀▀▀▀    ██      ██    ██  ██▀▀▀▀▀▀   ██       ██  ▀██▄  ██▀▀▀▀▀▀  ██        ██    ██  ██    ██           
 ▄██  ██▄  ▀██▄▄▄▄█    ██▄▄▄   ██    ██  ▀██▄▄▄▄█   ██       ██    ██  ▀██▄▄▄▄█  ▀██▄▄▄▄█  ▀██▄▄██▀  ██    ██           
 ▀▀    ▀▀    ▀▀▀▀▀      ▀▀▀▀   ▀▀    ▀▀    ▀▀▀▀▀    ▀▀       ▀▀    ▀▀▀   ▀▀▀▀▀     ▀▀▀▀▀     ▀▀▀▀    ▀▀    ▀▀                                                                                                                               
                                        {APP_NAME} - {APP_VERSION}
    """)

def parse_args():
    parser = argparse.ArgumentParser(
        description="AetherRecon - Modular OSINT & Reconnaissance Framework"
    )

    subparsers = parser.add_subparsers(dest="mode", help="Available modes")

    subdomain_parser = subparsers.add_parser("subdomain", help="Run subdomain enumeration")
    subdomain_parser.add_argument("target", help="Target domain (example.com)")
    subdomain_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    domain_parser = subparsers.add_parser("domain", help="Run domain reconnaissance")
    domain_parser.add_argument("target", help="Target domain (example.com)")
    domain_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    ip_parser = subparsers.add_parser("ip", help="Run IP reconnaissance")
    ip_parser.add_argument("target", help="Target IP address")
    ip_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    http_parser = subparsers.add_parser("http", help="Run HTTP analysis")
    http_parser.add_argument("target", help="Target URL (http://example.com)")
    http_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    return parser.parse_args()

def main():
    banner()
    args = parse_args()

    if not args.mode:
        print("[-] No mode selected. Use -h for help.")
        sys.exit(1)

    engine = Engine()

    if args.mode == "domain":
        result = engine.run_domain_analysis(args.target)

    elif args.mode == "subdomain":
        result = engine.run_subdomain(args.target)

    elif args.mode == "http":
        result = engine.analyze_http(args.target)

    elif args.mode == "ip":
        result = engine.run_ip_analysis(args.target)

    else:
        print("[-] Invalid mode selected.")
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=4))
    else:
        print(result)


if __name__ == "__main__":
    main()
