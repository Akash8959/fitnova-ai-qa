from app.repositories.transcript_repository import (
    TranscriptRepository,
)


class TranscriptionService:

    def __init__(
        self,
        provider,
        repository,
    ):
        self.provider = provider
        self.repository = repository

    def transcribe_call(self, call):

        existing = self.repository.get_by_call_id(call.id)

        if existing:
            print("Transcript already exists.")
            return existing

        result = self.provider.transcribe(
            call.file_path
        )

        transcript = self.repository.create(
            call_id=call.id,
            full_text=result["full_text"],
            language=result["language"],
            duration_seconds=result["duration"],
            segments=result["segments"],
        )

        print(
            f"Transcript stored for Call {call.id}"
        )

        return transcript