from pydantic import BaseModel, ConfigDict
from typing import Optional

class WritingPrincipleBase(BaseModel):
    risk_topic: str
    core_problem: Optional[str] = None
    guiding_principle: Optional[str] = None
    macro_strategy: Optional[str] = None
    micro_strategy: Optional[str] = None
    is_enabled: bool = True

class WritingPrincipleCreate(WritingPrincipleBase):
    pass

class WritingPrincipleUpdate(WritingPrincipleBase):
    pass

class WritingPrincipleInDB(WritingPrincipleBase):
    id: int
    project_id: str
    
    model_config = ConfigDict(from_attributes=True)

class WritingPrinciple(WritingPrincipleInDB):
    pass