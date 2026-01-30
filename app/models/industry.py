from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text
from app.core.database import Base

class Industry(Base):
    __tablename__ = "industries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("NOW()"))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("NOW()"), onupdate=text("NOW()"))
    
    leads = relationship("Lead", back_populates="industry")
