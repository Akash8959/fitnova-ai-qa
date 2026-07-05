class DiarizationService:

    def __init__(
        self,
        provider,
        repository,
    ):
        self.provider = provider
        self.repository = repository

    def diarize(self, transcript):

        segments = self.repository.get_segments(
            transcript.id
        )

        updates = self.provider.assign_speakers(
            segments
        )

        self.repository.update_speakers(
            updates
        )

        print(
            "Speaker labels assigned."
        )