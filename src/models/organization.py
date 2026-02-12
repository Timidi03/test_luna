from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Organization(Base):

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("buildings.id", ondelete="RESTRICT"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    building: Mapped["Building"] = relationship(
        "Building", back_populates="organizations"
    )
    activities: Mapped[List["Activity"]] = relationship(
        "Activity", back_populates="organizations", secondary="organization_activities"
    )
    phones: Mapped[List["Phone"]] = relationship(
        "Phone",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.name}, {self.building}, {self.activities}, {self.phones}"

    def __repr__(self):
        return f"{self.name}, {self.building}, {self.activities}, {self.phones}"
