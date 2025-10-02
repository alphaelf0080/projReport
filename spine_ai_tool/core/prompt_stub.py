GEMINI_SKELETON_PROMPT = """
You are an expert Spine 2D technical art assistant. Given a list of flattened layer names with optional type hints, infer:
1. Bone hierarchy (root anchored at 0,0) with logical parenting
2. Suggested slots (one per visible part unless mirrored)
3. Pivot refinements (0..1 relative factors)
4. Candidate simple procedural idle motions (breathing / head sway / limb micro-arc)
Return JSON keys: bones[], slots[], motions[]. Keep concise.
"""

def build_prompt(layer_names_with_types):
    items = "\n".join(f"- {n}: {t}" for n,t in layer_names_with_types)
    return GEMINI_SKELETON_PROMPT + "\nLayers:\n" + items + "\n"