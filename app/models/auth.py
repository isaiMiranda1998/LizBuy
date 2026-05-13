from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, DateTime, Boolean, ForeignKey
from app.db.base import Base
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .user import User

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    token_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")