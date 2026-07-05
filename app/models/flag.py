from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Flag(Base):
    __tablename__ = "flags"

    id = Column(Integer, primary_key=True, index=True)

    call_id = Column(
        Integer,
        ForeignKey("calls.id"),
        nullable=False,
    )

    issue_type = Column(
        String(100),
        nullable=False,
    )

    severity = Column(
        String(20),
        nullable=False,
    )

    timestamp_in_call = Column(
        String(20),
        nullable=False,
    )

    quoted_line = Column(
        Text,
        nullable=False,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    call = relationship(
        "Call",
        back_populates="flags",
    )