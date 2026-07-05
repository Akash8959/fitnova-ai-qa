from app.models.transcript_segment import TranscriptSegment


class TranscriptFormatter:
    @staticmethod
    def format(segments: list[TranscriptSegment]) -> str:
        lines = []

        for segment in segments:
            start = int(segment.start_time)
            hours = start // 3600
            minutes = (start % 3600) // 60
            seconds = start % 60

            timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"

            lines.append(
                f"[{timestamp}] {segment.speaker}: {segment.text.strip()}"
            )

        return "\n".join(lines)