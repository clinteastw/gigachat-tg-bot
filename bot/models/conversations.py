from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ForeignKey, delete, select


class Conversation(Base):
    __tablename__ = 'conversations'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    user_message: Mapped[str]
    assistant_message: Mapped[str]
    
    @classmethod
    async def get_history(cls, session: AsyncSession, user_tg_id: int) -> list["Conversation"]:
        """
        Get user conversation history.
        """
        stmt = await session.execute(
            select(cls).where(cls.user_tg_id == user_tg_id)
        )
        return stmt.scalars().all()

    @classmethod
    async def clear_history(cls, session: AsyncSession, user_tg_id: int) -> None:
        """
        Delete user conversation history.
        """
        await session.execute(
            delete(cls).where(cls.user_tg_id == user_tg_id)
        )
        await session.commit()

    @classmethod
    async def save_message(
        cls, session: AsyncSession, user_tg_id: int, user_message: str, assistant_message: str
    ) -> "Conversation":
        """
        Save user request and GigaChat assistant response
        """
        conversation = cls(
            user_tg_id=user_tg_id,
            user_message=user_message,
            assistant_message=assistant_message,
        )
        session.add(conversation)
        await session.commit()
        return conversation