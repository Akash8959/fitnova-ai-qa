from sqlalchemy.orm import Session

from app.models.call import Call


class CallResultsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_call(self, call_id: int):
        return (
            self.db.query(Call)
            .filter(Call.id == call_id)
            .first()
        )