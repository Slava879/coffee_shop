from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from coffee_shop.orders.models import Order
from coffee_shop.users.models import User

class OrderRepository:
    async def find_all(self, offset: int, limit: int, session: AsyncSession):
        q = select(Order).join(User).offset(offset).limit(limit)
        s = await session.execute(q)
        return s.scalars().all()
