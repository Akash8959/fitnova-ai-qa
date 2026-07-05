from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

    id = Column(Integer, primary_key=True, index=True)

    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id"),
        nullable=False,
    )

    speaker = Column(
        String(50),
        nullable=False,
        default="UNKNOWN",
    )

    start_time = Column(
        Float,
        nullable=False,
    )

    end_time = Column(
        Float,
        nullable=False,
    )

    text = Column(
        Text,
        nullable=False,
    )

    transcript = relationship(
        "Transcript",
        back_populates="segments",
    )