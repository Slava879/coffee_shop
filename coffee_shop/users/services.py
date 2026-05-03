from typing import Annotated

from coffee_shop.security.services import PasswordService
from coffee_shop.users.models import User
from coffee_shop.users.schemas import UserCreate, UserUpdate
from coffee_shop.users.repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Request

def get_user_service(request: Request) -> "UserService":
    return request.app.state.user_service

UserServiceDep = Annotated["UserService", Depends(get_user_service)]

class UserService:
    def __init__(self, user_repository: UserRepository, password_sevice: PasswordService):
        self.__repo = user_repository
        self.__pass_service = password_sevice

    async def register(self, user: UserCreate, session: AsyncSession) -> User:
        if await self.__repo.exists_by_login(user.login, session):
            raise HTTPException(status.HTTP_409_CONFLICT)
        
        user_model = User(login=user.login, password_hash=self.__pass_service)
        session.add(user_model)
        await session.commit()

    async def get_by_id(self, id: int) -> User: ...

    async def update_by_id(self, id: int, user: UserUpdate) -> User: ...
