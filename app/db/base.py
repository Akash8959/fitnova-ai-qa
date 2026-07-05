from app.db.database import Base

# Import all models here so Alembic can detect them

from app.models.organization import Organization
from app.models.team import Team
from app.models.advisor import Advisor
from app.models.call import Call
from app.models.transcript import Transcript
from app.models.score import Score
from app.models.flag import Flag
from app.models.transcript_segment import TranscriptSegment