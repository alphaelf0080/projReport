from loguru import logger
from .models import LayerMap, Bone, Slot
from typing import List

# Stub: 未接 Gemini，僅模擬推導骨架層級

def infer_bones_and_slots(layer_map: LayerMap):
    bones: List[Bone] = []
    slots: List[Slot] = []

    # root 保證存在
    if not any(l.name == 'root' for l in layer_map.layers):
        bones.append(Bone(name='root'))

    for l in layer_map.layers:
        parent = l.parent if l.parent != 'root' else 'root'
        bones.append(Bone(name=l.name, parent=parent))
        slots.append(Slot(name=f"{l.name}_slot", bone=l.name, attachment=l.name))

    logger.info(f"AI (stub) inferred {len(bones)} bones, {len(slots)} slots")
    return bones, slots
