from fastapi import APIRouter

from coffee_shop.core.db import SessionDep
from coffee_shop.security.dependencies import SecurityServiceDep
from coffee_shop.security.schemas import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login")
async def login(body: LoginRequest, service: SecurityServiceDep, session: SessionDep) -> LoginResponse:
    return await service.login(body, session)
