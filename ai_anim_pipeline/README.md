# AI Animation Pipeline (Gemini 2.5 + Veo 3) Skeleton

此專案為 Slot Game 動態資產自動化產生流程的最小可執行骨架 (A+B)。

## 目標
1. A: 建立結構化骨架（模組/階段/資料契約）。
2. B: 提供最小可跑 pipeline（dummy 實作，不呼叫真實 API）。

## 目前狀態
- 使用 `effects_catalog.yaml` 讀取動態效果需求
- 產生：
  - 偽 Prompt（plan 階段）
  - 偽影片檔 placeholder（generate 階段）
  - 偽評估指標（evaluate 階段）
  - 偽 spritesheet（pack 階段，用 Pillow 合成顏色塊）
  - `animation_manifest.json`
  - KPI 報告 (`reports/summary.md`)

## 依賴
見 `requirements.txt`

## 執行
```bash
pip install -r ai_anim_pipeline/requirements.txt
python ai_anim_pipeline/cli/run_pipeline.py
```

## 產出位置
```
ai_anim_pipeline/output/
  assets/                # spritesheet, meta
  reports/               # summary.md
  temp/                  # 中間檔
```

## 後續可擴充
- 接入 Gemini（plan / semantic evaluate）
- 接入 Veo 3（真實影片生成）
- Loop 誤差檢測 / Alpha 處理 / 壓縮
- 真實多變體 + 策略選擇

---
(Initial skeleton v1.0)
