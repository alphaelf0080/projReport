# Gemini 2.5 驅動的 Spine 2D Runtime 動畫產生工具（骨架）

此工具目標：
1. 輸入：一組靜態素材圖層（PNG / 已切好部件）或合成圖 + 元數據
2. AI（Gemini 2.5）分析：推導骨架層級（hierarchy）、pivot、關節名稱、可能的綁定點（attachment slots）
3. 產出：Spine 2D 兼容的 `skeleton.json` + 動畫初稿（如 idle / pulse / float）
4. 可再迭代：人為修改 + AI 建議更新

> 本階段為骨架 MVP：尚未串接真正 Gemini API 與 Spine Editor，自動輸出格式對齊 Spine JSON 結構（簡化）。

---
## 架構概覽
```
spine_ai_tool/
  config/
    layer_map_example.yaml      # 靜態素材對應規劃
  core/
    models.py                   # 資料模型
    ai_agent.py                 # Gemini 規劃（stub）
    analyzer.py                 # 圖層 / 圖像分析（占位）
    builder.py                  # Skeleton JSON 組裝
    anim_templates.py           # 預設程序動畫模板（idle / win_pose / hit_flash）
  cli/
    generate_from_layers.py     # 產出 skeleton JSON
    validate_spec.py            # 驗證 layer map 合法性
    export_hybrid_manifest.py   # 匯出影片 + skeleton 混合 manifest
    gen_prompt.py               # 生成 Gemini 骨架推導 Prompt (stub)
  samples/
    parts/                      # 示範圖層（可放空）
  output/
    skeleton/                   # 生成骨架 JSON
```

---
## 目標流程
1. 供應 `layer_map.yaml`：描述每個部件用途與父子關係（若缺少則 AI 推測）
2. `analyzer.py`：讀取圖檔尺寸 / 中心點 / 透明區域 bounding box
3. `ai_agent.py`：根據圖層命名 + 類型生成：
   - joint hierarchy (e.g., root → torso → head → leftArm → leftHand)
   - slot 列表（對應 attachment）
   - 預設 transform（scale=1, rotation=0）
4. `builder.py`：輸出簡化版 Spine JSON：`skeleton`, `bones`, `slots`, `skins`, `animations`
5. `anim_templates.py`：產出 procedural idle，例如：
   - head 小幅旋轉（-3° ↔ 3°）
   - 呼吸：torso Y scale 0.98 ↔ 1.02（2s 週期）
6. CLI 合併 → `output/skeleton/CHAR_demo_skeleton.json`

---
## Spine JSON（簡化參考）
```json
{
  "skeleton": { "hash": "", "spine": "4.1", "width": 0, "height": 0 },
  "bones": [ {"name": "root"}, {"name": "torso", "parent": "root"} ],
  "slots": [ {"name": "torso_slot", "bone": "torso", "attachment": "torso"} ],
  "skins": { "default": { "torso_slot": { "torso": {"x":0,"y":0,"width":256,"height":512} } } },
  "animations": { "idle": { "bones": { "torso": { "scale": [{"time":0,"x":1,"y":1},{"time":1,"x":1,"y":1.02},{"time":2,"x":1,"y":1}] } } } }
}
```

---
## 未來擴充方向
- 實際 Gemini 語意推導（部件角色分類 / 對稱偵測）
- 自動權重計算（若結合 mesh deform）
- 產出多段動畫（attack / win pose / damage flick）
- Spine 官方 runtime 驗證腳本
- 視覺化預覽（WebGL / Pixi / spine-ts）

## 執行（MVP 假資料）
```bash
pip install -r requirements.txt

# 生成骨架（相對路徑注意 out 目錄）
python spine_ai_tool/cli/generate_from_layers.py \
  --layer-map spine_ai_tool/config/layer_map_example.yaml \
  --out spine_ai_tool/output/skeleton/demo_skeleton.json

# 或使用模組方式（推薦）
python -m spine_ai_tool.cli.generate_from_layers \
  --layer-map spine_ai_tool/config/layer_map_example.yaml \
  --out spine_ai_tool/output/skeleton/demo_skeleton.json

# 驗證 layer map 結構
python -m spine_ai_tool.cli.validate_spec --layer-map spine_ai_tool/config/layer_map_example.yaml

# 匯出 Hybrid manifest（假設有一支核心影片 animations/symbol_core.webm）
python -m spine_ai_tool.cli.export_hybrid_manifest \
  --layer-map spine_ai_tool/config/layer_map_example.yaml \
  --video animations/symbol_core.webm \
  --out spine_ai_tool/output/hybrid/demo_hybrid.json

# 生成 Gemini 提示詞（用於 AI 推導骨架）
python -m spine_ai_tool.cli.gen_prompt --layer-map spine_ai_tool/config/layer_map_example.yaml --out spine_ai_tool/output/prompt.txt
```

---
(Initial Skeleton v0.1)
