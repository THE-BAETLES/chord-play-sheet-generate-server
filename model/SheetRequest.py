from pydantic import BaseModel
from typing import List
class SheetRequestModel(BaseModel):
    csv_path: str
    midi_path: str
    bpm: float
    beats: List[float]