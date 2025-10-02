from loguru import logger
from pathlib import Path
from ..core import PromptPlan, GenerationResult
import json, os

DUMMY_VIDEO_DIR = Path(__file__).parent.parent / 'output' / 'temp' / 'videos'

def run_variants(plan: PromptPlan):
    DUMMY_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for seed in plan.seed_list:
        variant_id = f"{plan.id}_seed{seed}"
        # 建立一個假檔案代表影片輸出
        video_path = DUMMY_VIDEO_DIR / f"{variant_id}.mp4"
        video_path.write_bytes(b"DUMMY_VIDEO")
        meta = {"model": "veo-3-dummy", "seed": seed}
        (DUMMY_VIDEO_DIR / f"{variant_id}.json").write_text(json.dumps(meta, indent=2))
        logger.info(f"[generate] fake video created: {video_path.name}")
        results.append(GenerationResult(
            plan_id=plan.id,
            variant_id=variant_id,
            seed=seed,
            video_path=str(video_path),
            raw_meta=meta
        ))
    return results
