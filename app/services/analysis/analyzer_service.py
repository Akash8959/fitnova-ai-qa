from app.services.analysis.guardrail import HallucinationGuardrail
from app.services.analysis.ollama_provider import OllamaProvider
from app.services.analysis.schemas import AnalysisResult
from app.services.analysis.transcript_formatter import TranscriptFormatter


class AnalyzerService:
    def __init__(
        self,
        provider: OllamaProvider,
        repository,
        guardrail=None,
    ):
        self.provider = provider
        self.repository = repository
        self.guardrail = guardrail or HallucinationGuardrail()

    def analyze_call(
        self,
        call,
    ) -> AnalysisResult:
        transcript = self.repository.get_by_call_id(
            call.id
        )

        if transcript is None:
            raise ValueError(
                f"No transcript found for call {call.id}"
            )

        segments = self.repository.get_segments(
            transcript.id
        )

        formatted = TranscriptFormatter.format(
            segments
        )

        result = self.provider.analyze(
            formatted
        )

        weights = {
            "needs_discovery": 25,
            "product_knowledge": 15,
            "objection_handling": 20,
            "compliance": 25,
            "next_step_booking": 15,
        }

        weighted_score = (
            (result.rubric.needs_discovery / 5)
            * weights["needs_discovery"]
            + (result.rubric.product_knowledge / 5)
            * weights["product_knowledge"]
            + (result.rubric.objection_handling / 5)
            * weights["objection_handling"]
            + (result.rubric.compliance / 5)
            * weights["compliance"]
            + (result.rubric.next_step_booking / 5)
            * weights["next_step_booking"]
        )

        result.weighted_score = round(
            weighted_score,
            2,
        )

        return self.guardrail.verify(
            result,
            segments,
        )