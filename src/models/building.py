from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, Float
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.organization import Organization


class Building(Base):

    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    address: Mapped[str] = mapped_column(TEXT, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    organizations: Mapped[List[Organization]] = relationship(
        Organization,
        back_populates="building",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.address}, lat={self.latitude}, lng={self.longitude}"

    def __repe__(self):
        return f"{self.address}, lat={self.latitude}, lng={self.longitude}"
