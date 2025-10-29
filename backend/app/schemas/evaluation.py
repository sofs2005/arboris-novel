from pydantic import BaseModel


class EvaluationResult(BaseModel):
    """A generic model for returning evaluation results."""
    project_id: str
    chapter_number: int
    result: str