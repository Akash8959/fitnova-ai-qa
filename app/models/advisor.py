from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Advisor(Base):
    __tablename__ = "advisors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    team_id = Column(
        Integer,
        ForeignKey("teams.id"),
        nullable=False,
    )

    team = relationship(
        "Team",
        back_populates="advisors",
    )

    calls = relationship(
        "Call",
        back_populates="advisor",
    )