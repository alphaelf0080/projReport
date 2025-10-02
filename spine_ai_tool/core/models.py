from __future__ import annotations
from pydantic import BaseModel
from typing import List, Dict, Optional

class LayerSpec(BaseModel):
    name: str
    file: str
    type: str
    parent: str
    pivot: Dict[str, float]

class IdleBreathing(BaseModel):
    target: str
    scaleY: float = 0.02
    period: float = 2.0

class IdleHeadSwing(BaseModel):
    target: str
    rotDeg: float = 3.0
    period: float = 2.4

class IdleAnimSpec(BaseModel):
    enable: bool = True
    breathing: Optional[IdleBreathing]
    headSwing: Optional[IdleHeadSwing]

class LayerMap(BaseModel):
    characterId: str
    layers: List[LayerSpec]
    animations: Dict[str, IdleAnimSpec]

class Bone(BaseModel):
    name: str
    parent: Optional[str] = None

class Slot(BaseModel):
    name: str
    bone: str
    attachment: str

class SpineSkeleton(BaseModel):
    skeleton: Dict
    bones: List[Bone]
    slots: List[Slot]
    skins: Dict
    animations: Dict
