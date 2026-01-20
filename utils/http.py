import requests
import re


TIMEOUT = 6
HEADERS = {
    "User-Agent": "AetherRecon/1.0"
}


def analyze_http(url: str) -> dict:
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        html = response.text.lower()

        title = None
        match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        if match:
            title = match.group(1).strip()

        return {
            "url": url,
            "alive": True,
            "status_code": response.status_code,
            "final_url": response.url,
            "title": title,
            "headers": dict(response.headers)
        }

    except requests.RequestException:
        return {
            "url": url,
            "alive": False,
            "status_code": None,
            "final_url": None,
            "title": None,
            "headers": {}
        }