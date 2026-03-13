import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}


def search_places(city: str, query: str) -> list[dict]:
    search_query = f"{query} in {city}"
    results = list(DDGS().text(search_query, max_results=6))

    places = []
    for r in results:
        places.append({
            "name": r.get("title", ""),
            "url": r.get("href", ""),
            "description": r.get("body", ""),
            "image_url": "",
        })

    return places


def fetch_image_url(url: str) -> str:
    try:
        full_url = url if url.startswith("http") else f"https://{url}"
        resp = requests.get(full_url, headers=HEADERS, timeout=4)
        soup = BeautifulSoup(resp.text, "html.parser")
        tag = soup.select_one('meta[property="og:image"]')
        if tag:
            content = tag.get("content", "")
            if content:
                return content
    except Exception:
        pass
    return ""
