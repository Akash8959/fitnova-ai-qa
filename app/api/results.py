from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.call_results_repository import CallResultsRepository

router = APIRouter(prefix="/results", tags=["Results"])


@router.get("/{call_id}")
def get_call_results(
    call_id: int,
    db: Session = Depends(get_db),
):
    repository = CallResultsRepository(db)

    call = repository.get_call(call_id)

    if call is None:
        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )

    transcript = []

    if call.transcript:
        segments = sorted(
            call.transcript.segments,
            key=lambda x: x.start_time,
        )

        for segment in segments:
            transcript.append(
                {
                    "speaker": segment.speaker,
                    "start_time": segment.start_time,
                    "end_time": segment.end_time,
                    "text": segment.text,
                }
            )

    score = None

    if call.score:
        score = {
            "needs_discovery": call.score.needs_discovery,
            "product_knowledge": call.score.product_knowledge,
            "objection_handling": call.score.objection_handling,
            "compliance": call.score.compliance,
            "next_step_booking": call.score.next_step_booking,
            "overall_score": call.score.overall_score,
        }

    flags = []

    for flag in call.flags:
        flags.append(
            {
                "issue_type": flag.issue_type,
                "severity": flag.severity,
                "timestamp_in_call": flag.timestamp_in_call,
                "quoted_line": flag.quoted_line,
                "reason": flag.reason,
            }
        )

    return {
        "call_id": call.id,
        "file_name": call.file_name,
        "language": call.transcript.language if call.transcript else None,
        "duration_seconds": call.transcript.duration_seconds if call.transcript else None,
        "score": score,
        "flags": flags,
        "transcript": transcript,
    }