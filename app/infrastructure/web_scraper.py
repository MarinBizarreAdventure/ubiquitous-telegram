import requests
from bs4 import BeautifulSoup

from app.domain.entities import Place
from app.domain.ports import ScraperPort


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


class WebScraper(ScraperPort):
    def search_places(self, city: str, query: str, place_type: str | None = None) -> list[Place]:
        search_query = f"{query} {place_type or ''} in {city}".strip()
        url = f"https://www.bing.com/search?q={requests.utils.quote(search_query)}"

        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        places = []

        for result in soup.select("li.b_algo")[:8]:
            title_tag = result.select_one("h2 a")
            snippet_tag = result.select_one("p")

            if not title_tag:
                continue

            name = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            description = snippet_tag.get_text(strip=True) if snippet_tag else ""

            places.append(
                Place(
                    name=name,
                    type=place_type or "place",
                    location=city,
                    description=description,
                    url=link,
                )
            )

        return places
