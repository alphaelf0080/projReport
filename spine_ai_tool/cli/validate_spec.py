import argparse, yaml
from pathlib import Path
from loguru import logger
from ..core.models import LayerMap

def validate(layer_map: LayerMap):
    errors = []
    names = {l.name for l in layer_map.layers}
    for l in layer_map.layers:
        if l.parent != 'root' and l.parent not in names:
            errors.append(f"Parent missing: {l.name} -> {l.parent}")
    if len(names) != len(layer_map.layers):
        errors.append("Duplicate layer names detected")
    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer-map', required=True)
    args = ap.parse_args()
    data = yaml.safe_load(Path(args.layer_map).read_text())
    lm = LayerMap(**data)
    errs = validate(lm)
    if errs:
        for e in errs:
            logger.error(e)
        raise SystemExit(1)
    logger.success("Layer map valid")

if __name__ == '__main__':
    main()
