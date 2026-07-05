from app.db.database import SessionLocal
from app.models.transcript import Transcript
from app.repositories.transcript_repository import (
    TranscriptRepository,
)
from app.services.diarization.diarization_service import (
    DiarizationService,
)
from app.services.diarization.heuristic_provider import (
    HeuristicProvider,
)


def main():

    db = SessionLocal()

    transcript = db.query(Transcript).first()

    repository = TranscriptRepository(db)

    provider = HeuristicProvider()

    service = DiarizationService(
        provider,
        repository,
    )

    service.diarize(transcript)

    db.close()


if __name__ == "__main__":
    main()