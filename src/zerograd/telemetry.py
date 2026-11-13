"""Validated authored-weight events and evidence references."""
import json
from typing import Literal
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, model_validator
from zerograd.core import replay

class WeightEvent(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    type: Literal['weight_write']
    tensor: str
    shape: tuple[int,int]
    coords: list[tuple[int,int,float]]
    formula: str
    zero_grad: Literal[True]
    before_sha256: str = Field(pattern='^[0-9a-f]{64}$')
    after_sha256: str = Field(pattern='^[0-9a-f]{64}$')

    @model_validator(mode='after')
    def coordinates(self):
        import math
        if min(self.shape)<=0: raise ValueError('nonpositive shape')
        seen=set()
        for i,j,v in self.coords:
            if (i,j) in seen: raise ValueError('duplicate authored coordinate')
            if not (0<=i<self.shape[0] and 0<=j<self.shape[1]) or not math.isfinite(v):
                raise ValueError('invalid coordinate/value')
            seen.add((i,j))
        return self

class WeightStream(BaseModel):
    model_config = ConfigDict(extra='forbid')
    schema_version: Literal['1.0']
    architecture: str
    seed: int
    events: list[WeightEvent]

    @model_validator(mode='after')
    def unique_ids(self):
        if len({e.id for e in self.events})!=len(self.events):raise ValueError('duplicate event id')
        return self

def validate_stream(path):
    obj=WeightStream.model_validate_json(Path(path).read_text(encoding='utf-8'))
    replay(obj.model_dump())
    return obj

def export_schema():
    Path('schemas').mkdir(exist_ok=True)
    Path('schemas/telemetry.schema.json').write_text(json.dumps(WeightStream.model_json_schema(),indent=2),encoding='utf-8')
