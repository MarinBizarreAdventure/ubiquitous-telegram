from app.domain.entities import Place
from app.domain.ports import ScraperPort


class PlaceSearchUseCase:
    def __init__(self, scraper: ScraperPort) -> None:
        self._scraper = scraper

    def search(self, city: str, query: str, place_type: str | None = None) -> list[Place]:
        return self._scraper.search_places(city, query, place_type)
