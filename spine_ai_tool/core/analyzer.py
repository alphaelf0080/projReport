from pathlib import Path
from typing import Dict
from loguru import logger
try:
    from PIL import Image
except ImportError:  # pillow optional at runtime
    Image = None

# 簡化：僅取得檔案存在與假 bounding box

def analyze_image(path: Path) -> Dict:
    info = {"exists": path.exists(), "width": 0, "height": 0, "bbox": [0,0,0,0]}
    if Image and path.exists():
        try:
            with Image.open(path) as im:
                w, h = im.size
                info.update({"width": w, "height": h, "bbox": [0,0,w,h]})
        except Exception as e:
            logger.warning(f"Failed to open {path}: {e}")
    return info
