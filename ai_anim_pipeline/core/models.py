from __future__ import annotations
from pydantic import BaseModel
from typing import List, Dict, Optional

class EffectSpec(BaseModel):
    id: str
    category: str
    resolution: str
    duration_sec: float
    fps: int
    loops: bool
    variant_count: int = 1
    qa_rules: Dict[str, float] = {}

class PromptPlan(BaseModel):
    id: str
    prompt: str
    negative_prompt: Optional[str] = None
    seed_list: List[int] = []
    tags: List[str] = []
    technical_notes: Dict[str, str] = {}

class GenerationResult(BaseModel):
    plan_id: str
    variant_id: str
    seed: int
    video_path: str
    raw_meta: Dict

class EvalResult(BaseModel):
    variant_id: str
    pass_flag: bool
    metrics: Dict[str, float]

class PackagingResult(BaseModel):
    spritesheet_path: Optional[str]
    webm_path: Optional[str]
    meta_json: Dict
