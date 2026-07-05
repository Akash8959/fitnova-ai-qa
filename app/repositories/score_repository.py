from sqlalchemy.orm import Session

from app.models.score import Score
from app.services.analysis.schemas import AnalysisResult


class ScoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_call_id(self, call_id: int):
        return (
            self.db.query(Score)
            .filter(Score.call_id == call_id)
            .first()
        )

    def create(
        self,
        call_id: int,
        result: AnalysisResult,
    ):
        score = self.get_by_call_id(call_id)

        if score:
            return score

        score = Score(
            call_id=call_id,
            needs_discovery=result.rubric.needs_discovery,
            product_knowledge=result.rubric.product_knowledge,
            objection_handling=result.rubric.objection_handling,
            compliance=result.rubric.compliance,
            next_step_booking=result.rubric.next_step_booking,
            overall_score=result.weighted_score,
        )

        self.db.add(score)
        self.db.commit()
        self.db.refresh(score)

        return score