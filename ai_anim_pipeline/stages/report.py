from pathlib import Path
from loguru import logger
import statistics
import json
from typing import List, Dict

REPORT_DIR = Path(__file__).parent.parent / 'output' / 'reports'

def generate(kpi_records: List[Dict], output_dir: str = None):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
    else:
        out = REPORT_DIR

    # 過濾有效指標
    brightness_vals = [r.get('brightnessAvg') for r in kpi_records if r.get('brightnessAvg') is not None]
    size_vals = [r.get('sizeKB') for r in kpi_records if r.get('sizeKB') is not None]

    summary = {
        'total': len(kpi_records),
        'brightness_avg': round(statistics.mean(brightness_vals), 3) if brightness_vals else None,
        'size_avg_kb': round(statistics.mean(size_vals), 2) if size_vals else None
    }

    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    md = ["# KPI Summary", "", f"Total Variants: {summary['total']}"]
    if summary['brightness_avg']:
        md.append(f"Average Brightness: {summary['brightness_avg']}")
    if summary['size_avg_kb']:
        md.append(f"Average Size (KB): {summary['size_avg_kb']}")
    (out / 'summary.md').write_text("\n".join(md))
    logger.info(f"[report] summary generated -> {out}")
    return summary
