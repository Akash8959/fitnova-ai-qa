from sqlalchemy.orm import Session

from app.models.transcript import Transcript
from app.models.transcript_segment import TranscriptSegment


class TranscriptRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_call_id(self, call_id: int):
        return (
            self.db.query(Transcript)
            .filter(Transcript.call_id == call_id)
            .first()
        )

    def create(
        self,
        call_id: int,
        full_text: str,
        language: str,
        duration_seconds: float,
        segments: list,
    ):

        transcript = Transcript(
            call_id=call_id,
            full_text=full_text,
            language=language,
            duration_seconds=duration_seconds,
        )

        self.db.add(transcript)
        self.db.flush()

        for segment in segments:
            self.db.add(
                TranscriptSegment(
                    transcript_id=transcript.id,
                    speaker="UNKNOWN",
                    start_time=segment["start"],
                    end_time=segment["end"],
                    text=segment["text"],
                )
            )

        self.db.commit()
        self.db.refresh(transcript)

        return transcript

    def get_segments(self, transcript_id: int):
        return (
            self.db.query(TranscriptSegment)
            .filter(
                TranscriptSegment.transcript_id == transcript_id
            )
            .order_by(TranscriptSegment.start_time)
            .all()
        )

    def update_speakers(self, updates: list):

        for item in updates:
            segment = (
                self.db.query(TranscriptSegment)
                .filter(
                    TranscriptSegment.id == item["id"]
                )
                .first()
            )

            if segment:
                segment.speaker = item["speaker"]

        self.db.commit()