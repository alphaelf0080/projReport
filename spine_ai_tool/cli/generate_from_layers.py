import argparse, yaml, json
from pathlib import Path
from loguru import logger
from ..core.models import LayerMap
from ..core.builder import build_skeleton


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer-map', required=True, help='YAML layer map path')
    ap.add_argument('--out', required=True, help='Output skeleton json path')
    args = ap.parse_args()

    layer_map_path = Path(args.layer_map)
    out_path = Path(args.out)

    data = yaml.safe_load(layer_map_path.read_text())
    layer_map = LayerMap(**data)

    skeleton_json = build_skeleton(layer_map)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(skeleton_json, indent=2))
    logger.success(f"Skeleton written -> {out_path}")

if __name__ == '__main__':
    main()
