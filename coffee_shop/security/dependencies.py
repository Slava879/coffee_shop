from typing import Annotated

from fastapi import Depends, Request
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from coffee_shop.users.models import User
from coffee_shop.security.services import SecurityService

SecuritySchema = HTTPBearer(auto_error=False)

def get_security_service(request: Request) -> SecurityService:
    return request.app.state.security_service

type SecurityServiceDep = Annotated[SecurityService, Depends(get_security_service)]

async def authenticate(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(SecuritySchema)
    ],
) -> User | None: ...


type AuthUser = Annotated[User | None, Depends(authenticate)]
