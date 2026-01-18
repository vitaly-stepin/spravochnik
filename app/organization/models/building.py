from datetime import datetime
from sqlalchemy import String, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Building(Base):
    """Модель для описания зданий, в которых располагаются организации. Many To Many связь."""
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    organizations: Mapped[list["Organization"]] = relationship(back_populates="building")

    __table_args__ = (
        Index("idx_buildings_coords", "latitude", "longitude"),
    )
