from math import isclose

DEFAULT_EASING = "cubicOut"

def build_idle_animation(spec):
    anim = {"bones": {}}
    idle = spec.animations.get('idle')
    if not idle or not idle.enable:
        return anim

    bones_section = {}
    # Breathing: scale Y cycle (0 -> period)
    if idle.breathing:
        b = idle.breathing
        bones_section.setdefault(b.target, {})
        bones_section[b.target].setdefault('scale', [])
        bones_section[b.target]['scale'] = [
            {"time": 0, "x": 1, "y": 1},
            {"time": b.period/2, "x": 1, "y": 1 + b.scaleY},
            {"time": b.period, "x": 1, "y": 1}
        ]
    # Head swing: rotation small oscillation
    if idle.headSwing:
        h = idle.headSwing
        bones_section.setdefault(h.target, {})
        bones_section[h.target].setdefault('rotate', [])
        bones_section[h.target]['rotate'] = [
            {"time": 0, "angle": 0},
            {"time": h.period/4, "angle": h.rotDeg},
            {"time": h.period/2, "angle": 0},
            {"time": h.period*3/4, "angle": -h.rotDeg},
            {"time": h.period, "angle": 0}
        ]
    anim["bones"] = bones_section
    return anim

def build_hit_flash(layer_map, duration=0.35, stagger=0.02):
    """Enhanced slot-level flash with stagger & intensity curve.

    Layer map can optionally define animations.hitFlash:
      hitFlash:
        enable: true
        duration: 0.4
        stagger: 0.015
        intensity: 0.55  # (0~1) controls mid flash dimming
    """
    cfg = None
    anim_def = getattr(layer_map, 'animations', {}) or {}
    raw = anim_def.get('hitFlash') if isinstance(anim_def, dict) else None
    if raw and isinstance(raw, dict):
        cfg = raw
        duration = cfg.get('duration', duration)
        stagger = cfg.get('stagger', stagger)
        intensity = max(0.1, min(0.95, cfg.get('intensity', 0.5)))
    else:
        intensity = 0.5

    base_times = [0, duration/6, duration/3, duration]
    mid_tint = int(0xFF * (1 - intensity * 0.6))
    mid_hex = f"ff{mid_tint:02x}{mid_tint:02x}{mid_tint:02x}"
    colors = ["ffffffff", mid_hex, "ffffffff", "ffffffff"]
    slots = {}
    for idx, layer in enumerate(layer_map.layers):
        slot_name = f"{layer.name}_slot"
        offset = idx * stagger
        slot_times = [min(duration, t + offset) for t in base_times]
        slot_times = sorted(set(round(t, 4) for t in slot_times))
        seq = []
        for t in slot_times:
            # nearest original index
            nearest_i = 0
            best = 999
            for bi, bt in enumerate(base_times):
                d = abs(t - min(duration, bt + offset))
                if d < best:
                    best = d
                    nearest_i = bi
            seq.append({"time": t, "color": colors[nearest_i]})
        slots[slot_name] = {"color": seq}
    return {"slots": slots}

def build_win_pose(layer_map):
    bones = {}
    # Slight celebratory lift/rotate for head and arms if present
    names = {l.name for l in layer_map.layers}
    if 'head' in names:
        bones['head'] = {"rotate": [
            {"time":0,"angle":0},{"time":0.2,"angle":5},{"time":0.6,"angle":2},{"time":1.0,"angle":0}
        ]}
    for arm in ('leftArm','rightArm'):
        if arm in names:
            bones[arm] = {"rotate": [
                {"time":0,"angle":0},{"time":0.3,"angle":8},{"time":0.8,"angle":3},{"time":1.2,"angle":0}
            ]}
    return {"bones": bones}

def _add_easing(anim):
    bones = anim.get('bones', {})
    for bone_name, tracks in bones.items():
        for prop, kfs in tracks.items():
            if isinstance(kfs, list):
                for k in kfs:
                    k.setdefault('curve', DEFAULT_EASING)
    slots = anim.get('slots', {})
    for slot_name, slot_tracks in slots.items():
        for prop, kfs in slot_tracks.items():
            if isinstance(kfs, list):
                for k in kfs:
                    k.setdefault('curve', 'linear')
    return anim

def _compress(anim, rot_thresh=0.1, scale_thresh=0.002):
    bones = anim.get('bones', {})
    for bone, tracks in bones.items():
        for prop, kfs in list(tracks.items()):
            if len(kfs) <= 2:
                continue
            filtered = [kfs[0]]
            for i in range(1, len(kfs)-1):
                prev, cur, nxt = kfs[i-1], kfs[i], kfs[i+1]
                if prop == 'rotate':
                    if abs((cur.get('angle',0) - prev.get('angle',0))) < rot_thresh and \
                       abs((nxt.get('angle',0)-cur.get('angle',0))) < rot_thresh:
                        continue
                if prop == 'scale':
                    if isclose(cur.get('x',1), prev.get('x',1), abs_tol=scale_thresh) and \
                       isclose(cur.get('y',1), prev.get('y',1), abs_tol=scale_thresh) and \
                       isclose(nxt.get('x',1), cur.get('x',1), abs_tol=scale_thresh) and \
                       isclose(nxt.get('y',1), cur.get('y',1), abs_tol=scale_thresh):
                        continue
                filtered.append(cur)
            filtered.append(kfs[-1])
            tracks[prop] = filtered
    return anim

ANIM_BUILDERS = {
    'idle': build_idle_animation,
    'hit_flash': build_hit_flash,
    'win_pose': build_win_pose
}

def build_all_animations(layer_map, apply_easing=True, compress=True):
    animations = {}
    idle = build_idle_animation(layer_map)
    if idle.get('bones'):
        if apply_easing: _add_easing(idle)
        if compress: _compress(idle)
        animations['idle'] = idle
    hf = build_hit_flash(layer_map)
    if apply_easing: _add_easing(hf)
    animations['hit_flash'] = hf
    wp = build_win_pose(layer_map)
    if wp.get('bones'):
        if apply_easing: _add_easing(wp)
        if compress: _compress(wp)
        animations['win_pose'] = wp
    return animations
