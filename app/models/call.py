from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    # Prevent duplicate ingestion
    source_id = Column(String(255), unique=True, nullable=False)

    # Original file name
    file_name = Column(String(255), nullable=False)

    # Full file path
    file_path = Column(String(500), nullable=False)

    # Audio format
    file_type = Column(String(20), nullable=False)

    advisor_id = Column(
        Integer,
        ForeignKey("advisors.id"),
        nullable=True,   # We'll assign advisor later
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    advisor = relationship(
        "Advisor",
        back_populates="calls",
    )

    transcript = relationship(
        "Transcript",
        back_populates="call",
        uselist=False,
    )

    score = relationship(
        "Score",
        back_populates="call",
        uselist=False,
    )

    flags = relationship(
        "Flag",
        back_populates="call",
    )