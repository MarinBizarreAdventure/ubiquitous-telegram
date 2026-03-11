from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.schemas import CreateUserRequest, UpdateUserRequest, UserResponse
from app.container import get_user_use_case
from app.use_cases.user import UserUseCase

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(body: CreateUserRequest, uc: UserUseCase = Depends(get_user_use_case)):
    user = uc.create_user(body.name, body.city, body.preferences)
    return UserResponse(id=user.id, name=user.name, city=user.city, preferences=user.preferences)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, uc: UserUseCase = Depends(get_user_use_case)):
    try:
        user = uc.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return UserResponse(id=user.id, name=user.name, city=user.city, preferences=user.preferences)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UpdateUserRequest, uc: UserUseCase = Depends(get_user_use_case)):
    try:
        user = uc.update_user(user_id, body.name, body.city, body.preferences)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return UserResponse(id=user.id, name=user.name, city=user.city, preferences=user.preferences)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, uc: UserUseCase = Depends(get_user_use_case)):
    try:
        uc.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
