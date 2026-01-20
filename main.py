import sys
import logging

from cli import main as cli_main
from core.config import DEBUG


def setup_logging():
    level = logging.DEBUG if DEBUG else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )


def main():
    setup_logging()

    try:
        cli_main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=DEBUG)
        sys.exit(1)


if __name__ == "__main__":
    main()
