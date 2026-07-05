from app.services.transcription.whisper_provider import (
    WhisperProvider,
)

provider = WhisperProvider()

text = provider.transcribe(
    "sample_calls/sample_call.mp3"
)

print(text)