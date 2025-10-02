from loguru import logger
from random import random
from ..core import GenerationResult, EvalResult, EffectSpec

# 偽評估：提供基礎結構，未做真實影片解析

def run_all(gen: GenerationResult, qa_rules: dict) -> EvalResult:
    brightness = 0.5 + (random() * 0.4)  # 0.5 ~ 0.9
    size_kb = 100 + (random() * 200)     # 100-300
    loop_error = 0.0
    metrics = {
        "brightnessAvg": brightness,
        "sizeKB": size_kb,
        "loopError": loop_error
    }
    pass_flag = True
    if qa_rules.get("max_brightness") and brightness > qa_rules["max_brightness"]:
        pass_flag = False
    if qa_rules.get("max_size_kb") and size_kb > qa_rules["max_size_kb"]:
        pass_flag = False
    if qa_rules.get("max_loop_error") and loop_error > qa_rules["max_loop_error"]:
        pass_flag = False
    logger.info(f"[evaluate] {gen.variant_id} -> pass={pass_flag} metrics={metrics}")
    return EvalResult(variant_id=gen.variant_id, pass_flag=pass_flag, metrics=metrics)
