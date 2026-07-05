import json

import httpx
from pydantic import ValidationError

from app.services.analysis.analyzer_provider import AnalyzerProvider
from app.services.analysis.prompt_builder import PromptBuilder
from app.services.analysis.schemas import AnalysisResult


class OllamaProvider(AnalyzerProvider):
    def __init__(
        self,
        model: str = "llama3.2:3b",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def analyze(self, transcript: str) -> AnalysisResult:
        prompt = PromptBuilder.build(transcript)

        for attempt in range(2):
            response = self._generate(prompt)

            try:
                return AnalysisResult.model_validate_json(response)

            except ValidationError as e:
                if attempt == 1:
                    raise ValueError(
                        f"Failed to generate valid analysis JSON.\n{e}"
                    )

                prompt = (
                    "Your previous response was invalid.\n\n"
                    "Every flag MUST contain:\n"
                    "- type\n"
                    "- severity\n"
                    "- timestamp_in_call\n"
                    "- quoted_line\n"
                    "- reason\n\n"
                    "The reason must never be empty.\n"
                    "The reason must explain why the quoted evidence triggered the flag.\n\n"
                    "Return ONLY valid JSON.\n\n"
                    + prompt
                )

    def _generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        return self._extract_json(data["response"])

    @staticmethod
    def _extract_json(text: str) -> str:
        text = text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON object found.")

        json.loads(text[start : end + 1])

        return text[start : end + 1]