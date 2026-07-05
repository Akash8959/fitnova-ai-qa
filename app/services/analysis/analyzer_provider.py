from abc import ABC, abstractmethod

from app.services.analysis.schemas import AnalysisResult


class AnalyzerProvider(ABC):
    @abstractmethod
    def analyze(self, transcript: str) -> AnalysisResult:
        raise NotImplementedError