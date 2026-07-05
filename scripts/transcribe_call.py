from app.db.database import SessionLocal
from app.models.call import Call
from app.repositories.transcript_repository import (
    TranscriptRepository,
)
from app.services.transcription.transcription_service import (
    TranscriptionService,
)
from app.services.transcription.whisper_provider import (
    WhisperProvider,
)


def main():

    db = SessionLocal()

    call = db.query(Call).first()

    provider = WhisperProvider()

    repository = TranscriptRepository(db)

    service = TranscriptionService(
        provider,
        repository,
    )

    service.transcribe_call(call)

    db.close()


if __name__ == "__main__":
    main()