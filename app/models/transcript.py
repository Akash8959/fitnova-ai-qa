from sqlalchemy import Column, Float, ForeignKey, Integer, Text, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)

    call_id = Column(
        Integer,
        ForeignKey("calls.id"),
        unique=True,
        nullable=False,
    )

    full_text = Column(
        Text,
        nullable=False,
    )

    language = Column(
        String(20),
        nullable=False,
    )

    duration_seconds = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    call = relationship(
        "Call",
        back_populates="transcript",
    )

    segments = relationship(
        "TranscriptSegment",
        back_populates="transcript",
        cascade="all, delete-orphan",
    )