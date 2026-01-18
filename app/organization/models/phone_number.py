from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class PhoneNumber(Base):
    """
        Модель для связи номеров телефона и организаций.
        Many To One связь: у одной организации мб более 1 номера телефона, телефон всегда принадлежит 1 организации.
    """
    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")

    __table_args__ = (
        Index("idx_phone_numbers_org_id", "organization_id"),
    )
