import json
from pathlib import Path
from .models import SpineSkeleton, LayerMap
from .ai_agent import infer_bones_and_slots
from .anim_templates import build_all_animations
from .analyzer import analyze_image


def build_skeleton(layer_map: LayerMap):
    bones, slots = infer_bones_and_slots(layer_map)

    skins = {"default": {}}
    for l in layer_map.layers:
        slot_name = f"{l.name}_slot"
        skins["default"].setdefault(slot_name, {})
        dims = analyze_image(Path(l.file)) if l.file else {"width":0,"height":0}
        skins["default"][slot_name][l.name] = {"x":0, "y":0, "width":dims.get('width',0), "height":dims.get('height',0)}

    animations = build_all_animations(layer_map, apply_easing=True, compress=True)

    skeleton_obj = SpineSkeleton(
        skeleton={"hash":"","spine":"4.1","width":0,"height":0},
        bones=bones,
        slots=slots,
        skins=skins,
        animations=animations
    )
    return json.loads(skeleton_obj.model_dump_json())
