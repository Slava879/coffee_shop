from fastapi import FastAPI
from coffee_shop.core.db import DatabaseManager
from contextlib import asynccontextmanager
from coffee_shop.users.services import UserService
from coffee_shop.security.services import PasswordService, SecurityService, TokenService
from datetime import timedelta
from coffee_shop.users.repositories import UserRepository

SECRET_KEY = '4545454534534354534534534534534354'

def setup_app():
    db_manager = DatabaseManager(
        "postgresql+asyncpg://admin:qwerty12@db:5432/coffee_shop"
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with db_manager:
            yield

    app = FastAPI(lifespan=lifespan)

    app.state.db_manager = db_manager
    user_repository = UserRepository()
    password_service = PasswordService()
    token_service = TokenService(SECRET_KEY, timedelta(minutes=5))
    app.state.user_service = UserService(user_repository, password_service)
    app.state.security_service = SecurityService(user_repository, password_service, token_service)

    from coffee_shop.security.routers import router as security_router
    from coffee_shop.users.routers import router as user_router

    app.include_router(security_router)
    app.include_router(user_router)

    return app
