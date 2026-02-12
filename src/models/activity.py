from typing import List

from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Activity(Base):

    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(TEXT, nullable=False, index=True, unique=True)
    path: Mapped[str] = mapped_column(String, nullable=False, index=True)

    organizations: Mapped[List["Organization"]] = relationship(
        "Organization", back_populates="activities", secondary="organization_activities"
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
