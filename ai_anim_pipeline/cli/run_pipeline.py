import yaml
from pathlib import Path
from loguru import logger
from rich.progress import track

from ..core import EffectSpec
from ..stages import plan, generate, evaluate, postprocess, pack, manifest, report

CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'effects_catalog.yaml'
OUTPUT_DIR = Path(__file__).parent.parent / 'output'


def load_effect_specs(path: Path):
    data = yaml.safe_load(path.read_text())
    specs = [EffectSpec(**e) for e in data.get('effects', [])]
    return specs


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    specs = load_effect_specs(CONFIG_PATH)
    logger.info(f"Loaded {len(specs)} effect specs")

    manifest_items = []
    kpi_records = []

    for spec in track(specs, description="Pipeline Running"):
        plan_obj = plan.build_prompt(spec)
        gens = generate.run_variants(plan_obj)
        accepted = None
        for g in gens:
            eval_res = evaluate.run_all(g, spec.qa_rules)
            if eval_res.pass_flag:
                processed = postprocess.process(g, spec)
                packaged = pack.package(processed, spec)
                manifest_items.append(packaged.meta_json)
                kpi_records.append(eval_res.metrics)
                accepted = g
                break
        if not accepted:
            kpi_records.append({"id": spec.id, "status": "NO_PASS"})

    manifest.write(manifest_items)
    report.generate(kpi_records)
    logger.success("Pipeline completed.")

if __name__ == "__main__":
    main()
