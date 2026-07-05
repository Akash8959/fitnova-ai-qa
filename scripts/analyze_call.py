from app.db.database import SessionLocal
from app.models.call import Call
from app.repositories.flag_repository import FlagRepository
from app.repositories.score_repository import ScoreRepository
from app.repositories.transcript_repository import TranscriptRepository
from app.services.analysis.analyzer_service import AnalyzerService
from app.services.analysis.guardrail import HallucinationGuardrail
from app.services.analysis.ollama_provider import OllamaProvider
from app.services.analysis.persistence_service import AnalysisPersistenceService


def main():
    db = SessionLocal()

    call = db.query(Call).first()

    if call is None:
        print("No call found.")
        db.close()
        return

    transcript_repository = TranscriptRepository(db)

    analyzer = AnalyzerService(
        provider=OllamaProvider(),
        repository=transcript_repository,
        guardrail=HallucinationGuardrail(),
    )

    result = analyzer.analyze_call(call)

    persistence = AnalysisPersistenceService(
        score_repository=ScoreRepository(db),
        flag_repository=FlagRepository(db),
    )

    score, flags = persistence.save(call, result)

    print("\nAnalysis completed successfully.\n")

    print(result.model_dump_json(indent=2))

    print(f"\nScore ID : {score.id}")
    print(f"Flags Stored : {len(flags)}")

    db.close()


if __name__ == "__main__":
    main()