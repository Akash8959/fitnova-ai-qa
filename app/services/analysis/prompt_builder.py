import textwrap


class PromptBuilder:
    @staticmethod
    def build(transcript: str) -> str:
        return textwrap.dedent(
            f"""
            You are an expert QA evaluator for FitNova, a phone-sales fitness coaching company.

            Evaluate the sales call using only the transcript provided.

            Score these dimensions from 1 to 5:

            - needs_discovery (25%)
            - product_knowledge (15%)
            - objection_handling (20%)
            - compliance (25%)
            - next_step_booking (15%)

            Calculate a weighted_score out of 100.

            Allowed flag types:

            - no_needs_discovery
            - over_promising
            - pressure_tactics
            - price_before_value
            - undisclosed_costs
            - weak_or_missing_trial_booking
            - talking_over_customer
            - non_sales_call

            Allowed severity values:

            - low
            - medium
            - high

            Every flag must contain:

            - type
            - severity
            - timestamp_in_call
            - quoted_line
            - reason

            The reason must be a non-empty sentence explaining why the quoted evidence triggered the selected flag.

            Never leave reason empty.
            

            Return ONLY valid JSON.

            Do not include markdown.

            Do not include explanations.

            Do not wrap JSON in ```.

            The JSON must exactly match this schema:

            {{
              "rubric": {{
                "needs_discovery": 1,
                "product_knowledge": 1,
                "objection_handling": 1,
                "compliance": 1,
                "next_step_booking": 1
              }},
              "weighted_score": 0,
              "flags": [
                {{
                  "type": "no_needs_discovery",
                  "severity": "medium",
                  "timestamp_in_call": "00:00:00",
                  "quoted_line": "...",
                  "reason": "..."
                }}
              ]
            }}

            Transcript

            {transcript}
            """
        ).strip()