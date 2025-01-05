from pydantic import BaseModel, Field


class ResumeScore(BaseModel):
    explanation: str = Field(
        title="Explanation",
        description="The explanation of the resume evaluation",
    )
    score: float = Field(
        title="Resume Score",
        description="The score of the resume evaluation",
    )
