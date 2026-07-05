from faster_whisper import WhisperModel

from app.services.transcription.provider import (
    TranscriptionProvider,
)


class WhisperProvider(TranscriptionProvider):

    def __init__(self):
        self.model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str):

        segments, info = self.model.transcribe(audio_path)

        transcript = []
        full_text = []

        for segment in segments:
            transcript.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
            )

            full_text.append(segment.text.strip())

        return {
            "language": info.language,
            "duration": info.duration,
            "full_text": " ".join(full_text),
            "segments": transcript,
        }