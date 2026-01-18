from sqlalchemy import String, Integer, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Activity(Base):
    """Модель для описания видов деятельности организаций. Many To Many связь."""
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    parent: Mapped["Activity | None"] = relationship(
        back_populates="children", remote_side="Activity.id"
    )
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activities", back_populates="activities"
    )

    __table_args__ = (
        Index("idx_activities_parent_id", "parent_id"),
        Index("idx_activities_name", "name"),
        CheckConstraint("level BETWEEN 1 AND 3", name="check_activity_level"),
    )
