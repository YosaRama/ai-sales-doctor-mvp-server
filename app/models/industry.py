from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Industry(Base):
    __tablename__ = "industries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default="NOW()")
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default="NOW()", onupdate="NOW()")
