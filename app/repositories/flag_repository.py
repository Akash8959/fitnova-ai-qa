from sqlalchemy.orm import Session

from app.models.flag import Flag
from app.services.analysis.schemas import AnalysisResult


class FlagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        call_id: int,
        result: AnalysisResult,
    ):
        flags = []

        for item in result.flags:
            flag = Flag(
                call_id=call_id,
                issue_type=item.type.value,
                severity=item.severity.value,
                timestamp_in_call=item.timestamp_in_call,
                quoted_line=item.quoted_line,
                reason=item.reason,
            )

            self.db.add(flag)
            flags.append(flag)

        self.db.commit()

        for flag in flags:
            self.db.refresh(flag)

        return flags