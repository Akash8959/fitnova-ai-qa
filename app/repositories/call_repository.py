from sqlalchemy.orm import Session

from app.models.call import Call


class CallRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_source_id(self, source_id: str):
        return (
            self.db.query(Call)
            .filter(Call.source_id == source_id)
            .first()
        )

    def create(self, **kwargs):
        call = Call(**kwargs)

        self.db.add(call)
        self.db.commit()
        self.db.refresh(call)

        return call