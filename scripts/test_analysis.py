from app.db.database import SessionLocal
from app.repositories.transcript_repository import TranscriptRepository
from app.services.analysis.ollama_provider import OllamaProvider
from app.services.analysis.transcript_formatter import TranscriptFormatter


def main():
    db = SessionLocal()

    repository = TranscriptRepository(db)

    transcript = repository.get_by_call_id(1)

    if transcript is None:
        print("Transcript not found.")
        return

    segments = repository.get_segments(transcript.id)

    formatted = TranscriptFormatter.format(segments)

    provider = OllamaProvider()

    result = provider.analyze(formatted)

    print(result.model_dump_json(indent=2))

    db.close()


if __name__ == "__main__":
    main()