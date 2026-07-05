from app.db.database import SessionLocal
from app.repositories.call_repository import CallRepository
from app.services.ingestion.folder_adapter import FolderAdapter
from app.services.ingestion.ingestion_service import IngestionService


def main():

    db = SessionLocal()

    repository = CallRepository(db)

    service = IngestionService(repository)

    adapter = FolderAdapter("sample_calls")

    calls = adapter.get_calls()

    for call in calls:
        service.ingest(call)

    db.close()


if __name__ == "__main__":
    main()