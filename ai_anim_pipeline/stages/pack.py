from loguru import logger
from pathlib import Path
from PIL import Image, ImageDraw
from ..core import PackagingResult, EffectSpec
import json
import random

ASSETS_DIR = Path(__file__).parent.parent / 'output' / 'assets'

# 產生一張顏色塊 spritesheet + meta json （假）

def package(processed: dict, spec: EffectSpec) -> PackagingResult:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    sheet_path = ASSETS_DIR / f"{spec.id}_sheet.png"
    meta_path = ASSETS_DIR / f"{spec.id}_sheet.json"

    # 建立一張 512x512 (或解析度拆寬高) 顏色塊圖片
    try:
        w, h = map(int, spec.resolution.lower().split('x'))
    except Exception:
        w, h = 512, 512
    img = Image.new('RGBA', (w, h), (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255))
    d = ImageDraw.Draw(img)
    d.text((10,10), spec.id, fill=(255,255,255,255))
    img.save(sheet_path)

    meta = {
        "id": spec.id,
        "frames": 1,
        "fps": spec.fps,
        "loops": spec.loops,
        "sheet": sheet_path.name
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    logger.info(f"[pack] sheet + meta generated for {spec.id}")
    return PackagingResult(
        spritesheet_path=str(sheet_path),
        webm_path=None,
        meta_json=meta
    )
