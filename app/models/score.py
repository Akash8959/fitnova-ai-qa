from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)

    call_id = Column(
        Integer,
        ForeignKey("calls.id"),
        unique=True,
        nullable=False,
    )

    needs_discovery = Column(
        Integer,
        nullable=False,
    )

    product_knowledge = Column(
        Integer,
        nullable=False,
    )

    objection_handling = Column(
        Integer,
        nullable=False,
    )

    compliance = Column(
        Integer,
        nullable=False,
    )

    next_step_booking = Column(
        Integer,
        nullable=False,
    )

    overall_score = Column(
        Float,
        nullable=False,
    )

    call = relationship(
        "Call",
        back_populates="score",
    )