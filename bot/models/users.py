from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class User(Base):
    __tablename__ = 'users'
    
    tg_id:Mapped[int] = mapped_column(primary_key=True)
    
    @classmethod
    async def get_or_create(cls, session: AsyncSession, tg_id: int) -> "User":
        """
        Get user by telegram ID if user does not exist creates new user.
        """
        user_stmt = await session.execute(
            select(cls).where(cls.tg_id == tg_id)
        )
        user = user_stmt.scalar_one_or_none()

        if not user:
            user = cls(tg_id=tg_id)
            session.add(user)
            await session.commit()  
        return user