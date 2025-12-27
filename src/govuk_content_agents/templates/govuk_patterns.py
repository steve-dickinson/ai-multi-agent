from typing import Dict, TypedDict, List

class ContentTemplate(TypedDict):
    name: str
    description: str
    structure: str
    prompt_guidance: str

GOVUK_TEMPLATES: Dict[str, ContentTemplate] = {
    "guide": {
        "name": "Detailed Guide",
        "description": "Explains a specific task or process in detail. Good for complex topics.",
        "structure": """
# [Title: Action-oriented, e.g., "Apply for..."]

[Summary: 140 chars max]

## Overview
[Context: Who this is for, what you get]

## Eligibility
[Bulleted list of requirements]

## How to [Action]
[Step by step instructions]

## After you [Action]
[What happens next]

## Contact
[Help details]
""",
        "prompt_guidance": "Focus on clarity and action. Use 'you' and 'your'. Keep sentences short."
    },
    "start_page": {
        "name": "Start Page",
        "description": "The entry point for a digital service. Must be simple and direct.",
        "structure": """
# [Service Name]

[Summary: What this service does]

## Use this service to:
* [Task 1]
* [Task 2]

## Before you start
You can cannot use this service if:
* [Condition 1]

You'll need:
* [Requirement 1]

[Start Button Placeholder]

## Other ways to apply
""",
        "prompt_guidance": "Crucial: List exactly what the user needs BEFORE they start. No fluff."
    },
    "answer": {
        "name": "Answer / Quick Answer",
        "description": "Immediate answer to a specific question (e.g., 'When are bank holidays?').",
        "structure": """
# [Question?]

[Direct Answer in 1-2 sentences]

## [Detail/Exception 1]
[Explanation]

## [Detail/Exception 2]
[Explanation]
""",
        "prompt_guidance": "Get to the point immediately. The first paragraph must answer the user's question."
    }
}
