from app.repositories.flag_repository import FlagRepository
from app.repositories.score_repository import ScoreRepository
from app.services.analysis.schemas import AnalysisResult


class AnalysisPersistenceService:
    def __init__(
        self,
        score_repository: ScoreRepository,
        flag_repository: FlagRepository,
    ):
        self.score_repository = score_repository
        self.flag_repository = flag_repository

    def save(
        self,
        call,
        result: AnalysisResult,
    ):
        score = self.score_repository.create(
            call.id,
            result,
        )

        flags = self.flag_repository.create(
            call.id,
            result,
        )

        return score, flags