from coffee_shop.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository:
    def __init__(self): ...

    async def find_by_id(self, id: int) -> User | None: ...

    async def exists_by_login(self, login: str, session: AsyncSession) -> bool:
        q = select(select(User).where(User.login == login).exists())
        s = await session.execute(q)
        return s.scalar_one()
    
    async def find_by_login(self, login: str, session: AsyncSession) -> User | None:
        q = select(User).where(User.login == login)
        s = await session.execute(q)
        return s.scalar_one_or_none()
