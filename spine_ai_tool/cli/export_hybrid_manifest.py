import argparse, json, yaml
from pathlib import Path
from loguru import logger
from ..core.models import LayerMap
from ..core.builder import build_skeleton

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer-map', required=True)
    ap.add_argument('--video', required=True, help='Path to core effect video (webm)')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    data = yaml.safe_load(Path(args.layer_map).read_text())
    lm = LayerMap(**data)
    skeleton = build_skeleton(lm)
    hybrid = {
        "type": "hybrid",
        "skeleton": skeleton,
        "video": args.video,
        "runtimeSpecMeta": {"layers": len(lm.layers)},
        "sync": {"offsetMs": 0}
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(hybrid, indent=2))
    logger.success(f"Hybrid manifest written -> {out_path}")

if __name__ == '__main__':
    main()
