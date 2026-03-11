from fastapi import APIRouter, Depends, HTTPException, Query

from app.adapters.api.schemas import PlaceResponse
from app.container import get_place_search_use_case
from app.use_cases.place_search import PlaceSearchUseCase

router = APIRouter(prefix="/api/places", tags=["places"])


@router.get("/search", response_model=list[PlaceResponse])
def search_places(
    city: str = Query(...),
    query: str = Query(...),
    type: str | None = Query(default=None),
    uc: PlaceSearchUseCase = Depends(get_place_search_use_case),
):
    try:
        places = uc.search(city, query, type)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search error: {str(e)}")
    return [
        PlaceResponse(
            name=p.name,
            type=p.type,
            location=p.location,
            description=p.description,
            url=p.url,
            rating=p.rating,
        )
        for p in places
    ]
