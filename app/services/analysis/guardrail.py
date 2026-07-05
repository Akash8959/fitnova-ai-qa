from rapidfuzz import fuzz

from app.services.analysis.schemas import AnalysisResult


class HallucinationGuardrail:
    def __init__(self, threshold: int = 80):
        self.threshold = threshold

    def verify(
        self,
        result: AnalysisResult,
        segments: list,
    ) -> AnalysisResult:
        verified_flags = []

        for flag in result.flags:
            best_score = 0
            best_segment = None

            for segment in segments:
                score = fuzz.partial_ratio(
                    flag.quoted_line.lower(),
                    segment.text.lower(),
                )

                if score > best_score:
                    best_score = score
                    best_segment = segment

            if (
                best_segment is not None
                and best_score >= self.threshold
            ):
                flag.quoted_line = best_segment.text
                flag.timestamp_in_call = self._format_time(
                    best_segment.start_time
                )
                verified_flags.append(flag)

        result.flags = verified_flags

        return result

    @staticmethod
    def _format_time(seconds: float) -> str:
        seconds = int(seconds)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"