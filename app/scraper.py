import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def search_places(city: str, query: str) -> list[dict]:
    search_query = f"{query} in {city}"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"

    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    places = []

    for result in soup.select(".result__body")[:6]:
        title_tag = result.select_one(".result__title")
        snippet_tag = result.select_one(".result__snippet")
        url_tag = result.select_one(".result__url")
        if not title_tag:
            continue
        places.append({
            "name": title_tag.get_text(strip=True),
            "url": url_tag.get_text(strip=True) if url_tag else "",
            "description": snippet_tag.get_text(strip=True) if snippet_tag else "",
        })

    return places
