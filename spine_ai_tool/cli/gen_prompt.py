import argparse, yaml
from pathlib import Path
from ..core.models import LayerMap
from ..core.prompt_stub import build_prompt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer-map', required=True)
    ap.add_argument('--out', required=False)
    args = ap.parse_args()
    data = yaml.safe_load(Path(args.layer_map).read_text())
    lm = LayerMap(**data)
    pairs = [(l.name, l.type) for l in lm.layers]
    prompt = build_prompt(pairs)
    if args.out:
        Path(args.out).write_text(prompt)
    else:
        print(prompt)

if __name__ == '__main__':
    main()