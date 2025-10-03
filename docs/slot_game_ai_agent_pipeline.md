# Slot Game AI Agent 製作流程與 SOP

## 版本資訊
- 版本：v1.0
- 建立日期：2025-10-03
- 文件性質：端到端製作流程（概念 → 數學 → 素材 → 動效 → 整合 → 驗證）
- 適用對象：企劃 / 美術 / 數學設計 / 動效 / 前端 / PM / 技術整合

---
## 🎯 目標
以 AI 代理（AI Agents）協助 Slot Game 開發全流程：自動化重複工作、建立統一規格、加速審核回圈，讓人類專注於創意與決策。

---
## 👥 AI 代理角色與分工
| 代理名稱 | 任務 | 主要輸入 | 主要輸出 | 人類介入 |
|-----------|------|----------|----------|----------|
| ConceptArtAgent | 主視覺 / Symbol 風格探索 | 主題、品牌調性 | key_visual_*、concept_batch | Art Lead 選擇路線 |
| DesignParserAgent | 解析企劃書結構 | 企劃書文本 | game_structure.json | 企劃確認 |
| MathModelAgent | 權重 / RTP 模擬 | game_structure.json | math_model.json, simulation_report | 數學驗證 |
| PSDAnalyzerAgent | 圖層轉規格 | PSD 原始檔 | art_spec.json | TA 校對 |
| AssetGenAgent | 靜態素材生成 | art_spec.json, style_guide | symbols/*.png | 美術審核 |
| PromptOptimizerAgent | Prompt 改良 | 原始 Prompt, 失敗樣本 | 最佳化 Prompt | Art Lead 核准 |
| VFXSpecAgent | 動效規格生成 | symbol meta | vfx_spec.json | 動效調整 |
| VFXGenAgent | 動效素材輸出 | vfx_spec.json | frames / spine / Lottie | 動效審核 |
| EngineIntegrationAgent | 整合與輸出 | spec / assets / math | manifest / slot_config.json | 前端驗證 |
| SimulationAgent | 自動測試 | config, math_model | validation_report.html | QA 評估 |
| AuditAgent | 流程紀錄 / 追溯 | 所有中介產物 | decision_log.json | PM / 稽核 |

---
## 🔁 全流程 12 階段細節

### 1. 產生 Concept Art 與主視覺
- 輸入：主題、品牌語氣、競品參考
- AI：產生 6–12 組方向 + 色票 + 構圖註解
- 輸出：`concept_batch_v1/`、`style_guide.md`
- 風格一致性指標：embedding ≥ 0.80

### 2. 概念與主視覺審核
- AI：依選定方向進行細化、局部增強、光效處理
- 比對：前後差異報告（結構/飽和度/對比）
- 人類：選擇最終主視覺 → `key_visual_final.png`

### 3. 解析企劃書 → 生成 PSD 設計結構
- AI：解析盤面結構、Symbol 類別、特色機制
- 產出：`game_structure.json`、`psd_plan.json`
- 可選：自動生成「圖層占位 PSD」

### 4. 生成數學模型、遊戲邏輯、假資料與模擬
- AI：計算初始權重 → 模擬 100k–1M spins
- 自動調參直到 RTP 偏差 ≤ 1%
- 輸出：`math_model.json`、`simulation_report.html`、`fake_spins_sample.csv`

### 5. PSD → 美術素材規格 JSON
- AI：解析圖層 → 正規化命名 → 分類（背景/UI/Symbol/特效占位）
- 輸出：`art_spec.json`（尺寸 / 狀態 / 合圖規則）
- 檢查：命名規範、透明度、重複圖層

### 6. 規格 → 靜態素材生成 / Prompt 建議
- AI：根據規格 + 風格指南生成多變體
- 生成符號狀態：normal / glow / hit / disable
- 輸出：`/assets/symbols/*.png`、`prompt_suggestions.json`

### 7. 靜態素材審核
- AI：embedding 比對風格、尺寸檢查、邊緣清晰度、色彩一致性
- 人類：只審「低分或異常標記」
- 輸出：`static_review_report.json`

### 8. 動態特效規格生成
- AI：基於符號屬性生成 timeline（粒子/殘影/光暈）
- 輸出：`vfx_spec.json`（timeline、事件、顏色、節奏）

### 9. 動態特效素材生成 / Prompt 建議
- AI：輸出動態序列 / Spine JSON / Lottie / SpriteSheet
- 品質檢查：幀間閃爍、亮度跳動
- 輸出：`/vfx/exports/*`、`vfx_manifest.json`

### 10. 動態素材審核
- AI：FrameDiff / 色彩波動指標
- 人類：調整節奏、過度流暢性
- 輸出：`vfx_review_report.json`

### 11. 整合 MCP / 前端引擎
- AI：生成 `assets_manifest.json`、`slot_config.json`
- 自動檢查：缺失資產、路徑錯誤、未引用資源
- 可產出自動 Demo Spin 頁面 (HTML)

### 12. 接入資料測試
- AI：模擬 10k / 50k Spins → 驗證 RTP、Feature 觸發率
- 產出：`integration_validation_report.html`
- Audit：decision log + 資產 hash

---
## 📂 建議目錄結構
```
slot_project/
  docs/
  design/
  specs/
  assets/
  vfx/
  integration/
  audit/
  reports/
```

---
## ✅ 契約 (Contract) 摘要
| Step | Input | Output | 檢查點 | 失敗處理 |
|------|-------|--------|--------|----------|
| 1 | 主題 | concept_batch | 風格分散度 | 重新生成 topN |
| 3 | 企劃書 | game_structure.json | 缺欄位 | 人工補填 |
| 4 | 結構 JSON | math_model.json | RTP 偏差 | 自動調整 |
| 5 | PSD | art_spec.json | 命名錯誤 | 正規化 |
| 6 | spec | symbols/ | 色偏 | 色票修正 |
| 8 | symbols meta | vfx_spec.json | 時間重疊 | timeline 重排 |
| 11 | specs+assets | manifest | 缺資產 | 報表警示 |
| 12 | config | validation_report | RTP 偏差 | 回溯第 4 步 |

---
## 📊 KPI 指標
| 指標 | 目標 |
|------|------|
| 風格一致性 | ≥ 0.85 |
| RTP 收斂迭代 | ≤ 5 次 |
| 靜態人工審核率 | < 30% |
| 動效異常幀率 | < 1% |
| Prompt 平均迭代 | ≤ 3 |
| 整合錯誤次數 | ≤ 1 / 版本 |
| RTP 偏差 | ≤ 0.5% |
| 開發週期縮短 | ≥ 50% |

---
## ⚠️ 風險與緩解
| 風險 | 描述 | 緩解 |
|------|------|------|
| 風格漂移 | 不同批次色調差 | 嵌入比對 + 色票鎖定 |
| Prompt 冗長 | Artifact 出現 | Token 權重分析 |
| PSD 混亂 | 規格失敗 | 自動命名正規化 |
| RTP 偏差大 | 權重估錯 | 自動再模擬 |
| 動效閃爍 | 幀品質不穩 | FrameDiff 檢測重生 |
| 資產缺漏 | manifest 不完整 | 自動掃描 hash |
| 追溯困難 | 版本混淆 | decision_log.json |

---
## 🧠 Prompt 模板示例
靜態符號：
```
[主題] slot symbol of [元素], stylized, 256x256, clean edges, high clarity, no watermark, transparent background
```
動態特效：
```
Generate JSON timeline for [symbol] hit effect: phases: charge(0-120ms gold glow), burst(120-240ms particles 24 spread 45deg), fade(240-300ms).
```
數學模型：
```
Given target RTP:[96.2], reels:5x3, symbols:[...], produce weightMatrix + simulate 100k spins + adjust if deviation >0.5%.
```

---
## 🚀 導入優先順序建議
1. 數學模型與企劃解析（Step 3/4）
2. PSD → 規格化（Step 5）
3. 靜態素材生成 + 審核（Step 6/7）
4. 動態特效（Step 8–10）
5. 整合與驗證（Step 11/12）

---
## 🗂 Audit 紀錄範例（decision_log.json）
```json
{
  "timestamp": "2025-10-03T10:22:00Z",
  "action": "math_model_update",
  "rpt_target": 0.962,
  "rpt_observed": 0.958,
  "adjustment": "increase Wild weight +2%",
  "operator": "MathModelAgent",
  "approved_by": "math_designer"
}
```

---
## 📌 未來增強
- 自動差異視覺化 (Diff UI)
- 生成式動效物理參數優化 (基於 RL)
- 玩家行為資料回饋調整權重
- 多模型 Prompt Ensembling

---
文件完。
