from loguru import logger
from pathlib import Path
from ..core import GenerationResult, EffectSpec

# 偽後處理：僅複製檔案並標記已處理

def process(gen: GenerationResult, spec: EffectSpec):
    out_dir = Path(__file__).parent.parent / 'output' / 'temp' / 'processed'
    out_dir.mkdir(parents=True, exist_ok=True)
    marker = out_dir / f"{gen.variant_id}_processed.flag"
    marker.write_text("processed")
    logger.info(f"[postprocess] processed marker created for {gen.variant_id}")
    return {"processed_flag": str(marker)}
