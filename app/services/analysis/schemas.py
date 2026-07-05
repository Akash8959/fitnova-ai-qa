from enum import Enum

from pydantic import BaseModel, Field


class FlagType(str, Enum):
    no_needs_discovery = "no_needs_discovery"
    over_promising = "over_promising"
    pressure_tactics = "pressure_tactics"
    price_before_value = "price_before_value"
    undisclosed_costs = "undisclosed_costs"
    weak_or_missing_trial_booking = "weak_or_missing_trial_booking"
    talking_over_customer = "talking_over_customer"
    non_sales_call = "non_sales_call"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RubricScores(BaseModel):
    needs_discovery: int = Field(..., ge=1, le=5)
    product_knowledge: int = Field(..., ge=1, le=5)
    objection_handling: int = Field(..., ge=1, le=5)
    compliance: int = Field(..., ge=1, le=5)
    next_step_booking: int = Field(..., ge=1, le=5)


class IssueFlag(BaseModel):
    type: FlagType
    severity: Severity
    timestamp_in_call: str
    quoted_line: str
    reason: str = Field(
        ...,
        min_length=1,
        strip_whitespace=True,
    )


class AnalysisResult(BaseModel):
    rubric: RubricScores
    weighted_score: float = Field(..., ge=0, le=100)
    flags: list[IssueFlag]