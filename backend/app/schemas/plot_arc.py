from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlotArcBase(BaseModel):
    description: str
    status: str = "unresolved"
    start_chapter_id: Optional[int] = None
    resolved_chapter_id: Optional[int] = None

class PlotArcCreate(PlotArcBase):
    pass

class PlotArcUpdate(PlotArcBase):
    pass

class PlotArcInDB(PlotArcBase):
    id: int
    project_id: str
    
    model_config = ConfigDict(from_attributes=True)

class PlotArc(PlotArcInDB):
    pass