from pathlib import Path
import json
from loguru import logger
from typing import List

MANIFEST_PATH = Path(__file__).parent.parent / 'output' / 'assets' / 'animation_manifest.json'

def write(items: List[dict], output: str = None):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": "v0.1-skeleton",
        "count": len(items),
        "assets": items
    }
    path = Path(output) if output else MANIFEST_PATH
    path.write_text(json.dumps(manifest, indent=2))
    logger.info(f"[manifest] written {len(items)} assets -> {path}")
    return path
