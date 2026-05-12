from dataclasses import dataclass


@dataclass
class EscalationResult:
    confidence: str
    escalation_required: bool
    reasons: list[str]


# Thresholds and keywords — edit here to update business rules
ESCALATION_KEYWORDS = [
    "mold",
    "multiple carriers",
    "unclear policy",
]

ESCALATION_FINANCIAL_TRIGGERS = [
    "$25,000",
    "$50,000",
    "$100,000",
]


def evaluate(combined_text: str) -> EscalationResult:
    text_lower = combined_text.lower()
    reasons = []

    for keyword in ESCALATION_KEYWORDS:
        if keyword in text_lower:
            reasons.append(f"Detected keyword: '{keyword}'")

    for trigger in ESCALATION_FINANCIAL_TRIGGERS:
        if trigger in combined_text:
            reasons.append(f"High financial exposure detected: {trigger}")

    if reasons:
        return EscalationResult(
            confidence="Medium",
            escalation_required=True,
            reasons=reasons
        )

    return EscalationResult(
        confidence="High",
        escalation_required=False,
        reasons=[]
    )


def format_escalation_reasons(result: EscalationResult) -> str:
    return "\n".join(f"- {r}" for r in result.reasons)