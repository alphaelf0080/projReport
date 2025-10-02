from loguru import logger
from typing import List
from ..core import EffectSpec, PromptPlan
import random

PROMPT_TEMPLATES = {
    "symbolWin": "Generate a short slot symbol win animation for {id}. Energetic burst, subtle scale pulse (8%), golden light sweep. {duration}s @ {fps}fps.",
    "backgroundLoop": "Create a seamless atmospheric loop background for {id}. Soft ambient motion, subtle depth fog. {duration}s @ {fps}fps loop.",
}

def build_prompt(spec: EffectSpec) -> PromptPlan:
    template = PROMPT_TEMPLATES.get(spec.category, PROMPT_TEMPLATES["symbolWin"])  # fallback
    prompt = template.format(id=spec.id, duration=spec.duration_sec, fps=spec.fps)
    seed_list = random.sample(range(1000, 9999), spec.variant_count)
    logger.info(f"[plan] {spec.id} prompt built. seeds={seed_list}")
    return PromptPlan(
        id=spec.id,
        prompt=prompt,
        seed_list=seed_list,
        tags=[spec.category],
        technical_notes={"loops": str(spec.loops)}
    )
