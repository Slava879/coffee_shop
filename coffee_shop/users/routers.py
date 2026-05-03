from fastapi import APIRouter

from coffee_shop.core.db import SessionDep
from coffee_shop.users.schemas import UserCreate, UserSchema, UserUpdate
from coffee_shop.users.services import UserServiceDep

router = APIRouter(prefix="/users")


@router.post("/register")
async def register(
    user: UserCreate, service: UserServiceDep, session: SessionDep
    ) -> UserSchema:
    user_model = await service.register(user, session)
    return UserSchema.model_validate(user_model)

@router.get("/me")
async def get_me() -> UserSchema: ...


@router.put("/me")
async def update_me(user: UserUpdate) -> UserSchema: ...
