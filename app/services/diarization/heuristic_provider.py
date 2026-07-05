from app.services.diarization.provider import (
    DiarizationProvider,
)


class HeuristicProvider(DiarizationProvider):

    def assign_speakers(self, segments):

        updated_segments = []

        for index, segment in enumerate(segments):

            speaker = (
                "Speaker A"
                if index % 2 == 0
                else "Speaker B"
            )

            updated_segments.append(
                {
                    "id": segment.id,
                    "speaker": speaker,
                }
            )

        return updated_segments