from fastapi import HTTPException, status

from coffee_shop.users.repositories import UserRepository
from coffee_shop.security.schemas import LoginRequest, LoginResponse
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

class PasswordService:
    def __init__(self):
        self.__context = CryptContext(schemes=['argon2'])

    def get_password_hash(self, password: str):
        return self.__context.hash(password)

    def compare_passwords(self, raw_password: str, password_hash: str):
        return self.__context.verify(raw_password, password_hash)

class TokenService:
    def __init__(self, secret_key: str, lifetime: timedelta):
        self.__secret_key = secret_key
        self.__lifetime = lifetime

    def issue_token(self, user_id: int):
        return jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.now() + self.__lifetime,
            },
            key=self.__secret_key,
        )

    def verify_token(self, token: str) -> int | None:
        try:
            payload = jwt.decode(token)
            return payload["user_id"]
        except jwt.InvalidTokenError:
            return None


class SecurityService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
    ): 
        self.__user_repo = user_repository
        self.__pass_service = password_service
        self.__token_service = token_service

    async def login(self, body: LoginRequest, session: AsyncSession) -> LoginResponse:
        user = await self.__user_repo.find_by_login(body.login, session)
        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        correct = self.__pass_service.compare_passwords(body.password, user.password_hash)

        if not correct:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        
        token = self.__token_service.issue_token(user.id)
        return LoginResponse(token=token)
