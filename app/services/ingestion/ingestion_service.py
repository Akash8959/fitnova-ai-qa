from app.repositories.call_repository import CallRepository


class IngestionService:

    def __init__(self, repository):
        self.repository: CallRepository = repository

    def ingest(self, call_data):

        existing = self.repository.get_by_source_id(
            call_data["source_id"]
        )

        if existing:
            print(
                f"Duplicate call detected: {call_data['source_id']}"
            )
            return existing

        call = self.repository.create(
            source_id=call_data["source_id"],
            file_name=call_data["file_name"],
            file_path=call_data["file_path"],
            file_type=call_data["file_type"],
        )

        print(f"Inserted Call ID: {call.id}")

        return call