from abc import ABC, abstractmethod


class DiarizationProvider(ABC):

    @abstractmethod
    def assign_speakers(self, segments):
        pass