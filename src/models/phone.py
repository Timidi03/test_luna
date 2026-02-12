from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Phone(Base):

    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="phones"
    )

    def __str__(self):
        return f"{self.phone_number}"

    def __repr__(self):
        return f"{self.phone_number}"
