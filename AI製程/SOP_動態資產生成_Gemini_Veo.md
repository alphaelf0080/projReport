# 🌀 Slot Game 動態資產生成整合 SOP（Gemini 2.5 + Veo 3）

**版本**: v1.0  
**日期**: 2025-10-03  
**適用角色**: 技術美術 (TA)、動態特效 (VFX)、客製工具工程、系統整合、AI Pipeline 工程  
**核心 AI 引擎**: Gemini 2.5（規劃/評估）、Veo 3（影片/動態生成）

> 目標：利用 Gemini 2.5（規劃 / Prompt 工程 / 評估 / 自動腳本生成）與 Veo 3（高品質影片/動態生成）組成 AI Agent Pipeline，自動化產出 Slot Game 所需的「符號動畫、連線效果、聽牌（Near-Miss）效果、背景循環動畫、轉場動畫、贏分(Big Win / Mega Win) 演出、結算畫面動態」等多類型動態資產，並確保一致性、可維護性與效能合格。

---
## 1. 動態資產分類與輸出規格
| 類型 | 目的 | 典型時長 | 目標 FPS | 尺寸 / 比例 | 輸出格式 (優先序) | 備註 |
|------|------|----------|---------|-------------|-------------------|------|
| 符號待機 (Idle) | Slot Reel 靜置微動 | 0.8–1.2s 循環 | 24 / 30 | 512x512 / 768x768 | PNG Sprite Sheet > WebP Sequence | 不可喧賓奪主，≤ 8–12 帧 |
| 符號命中 (Symbol Win) | 單圖中獎強調 | 0.6–0.9s | 30 | 同符號原尺寸 | PNG Sequence / APNG / WebM (alpha) | 支援亮度 / 外發光 / 粒子覆蓋 |
| 連線效果 (Line Win) | 突顯線路與倍數 | 0.8–1.2s | 30 | 線條覆蓋層 (1920x1080) | WebM (alpha) / Lottie / JSON VFX | 可程式化參數化顏色 |
| 聽牌效果 (Near-Miss / Tease) | 提升期待 | 1.0–1.4s | 30 | Reel 區域裁切 | WebM (alpha) + 補間程式光效 | 聲音同步點標記 |
| 背景循環 (Loop BG) | 氛圍 | 4–8s Loop | 24 | 1920x1080 / 2160x1080 | WebM VP9 / H.265 | Loop Seam ≤ 1 frame 色差 |
| Free Spin 轉場 | Base → Feature | 1.5–2.5s | 30 | 全螢幕 | WebM (alpha 分層) | 分離「前景 FX」、「遮罩」、「Logo」 |
| Big / Mega Win 演出 | 情緒爆發 | 2.0–3.0s | 30 | 全螢幕 / 中央聚焦 | WebM (alpha) + Sprite Overlay | 支援動態金幣疊加層 |
| 結算畫面 (Result Panel) | 回饋總贏分 | 1.2–2.0s | 30 | 面板區域 | WebM + 數字逐位動畫 | 需提供數字跳動曲線 |

---
## 2. 系統角色與責任
| Agent / 模組 | 責任 | 工具 |
|---------------|------|------|
| Gemini 2.5 規劃 Agent | 需求 → 規格拆解 / 指令模板自動生成 | Gemini 2.5 Flash / Pro |
| Gemini 2.5 評估 Agent | 自動對生成影片做規格比對、語義/敘述一致性檢查 | Gemini 2.5 |
| Veo 3 生成引擎 | 高品質影片 / 動態生成 (含 camera / lighting / material) | Veo 3 |
| 後處理管線 (FFmpeg + Python) | 切帧 / Loop 無縫 / Alpha 合成 / 壓縮 | ffmpeg / OpenCV |
| Sprite Sheet 打包 | 合併序列幀、壓縮、產生 meta JSON | 自動腳本 (Python) |
| 效能分析模組 | 計算體積 / 顯存 / 預載策略 | 自動腳本 (Python) |

---
## 3. 端到端流程總覽
```
需求收集 → 動態分類 → Gemini 規格草稿 → Prompt 模板化 → Veo 3 初稿生成
→ 自動評估 (解析度/時長/語義/亮度區間) → 後處理 (裁切/Loop/壓縮)
→ Sprite Sheet / WebM 封裝 → 整合 manifest.json → 引擎預覽驗證 → QA 簽核 → 發佈
```

---
## 4. 詳細執行步驟
1. 需求收集：從美術規格書 + 玩法流程圖抽取必需動態點 (Reel State, Win States, Feature Entry, Payout Summary)。  
2. 動態分類映射：建立 `effects_catalog.yaml`，列出每種效果的 `id / category / trigger_event / layering / priority`。  
3. Gemini 拆解：輸入需求 → 產出每類動態的「語意描述 + 視覺要素矩陣」。  
4. Prompt 模板化：對應資產類型套用模板（見第 6 節）。  
5. Veo 3 生成：批次送出（支援溫度 / 種子 / 相機運動參數變體 3–5 組）。  
6. 自動初篩：丟棄解析度錯誤、主體偏移 > 15% 安全區、平均亮度落差 > ±25% 基準。  
7. 後處理：Loop 修補 / Alpha 擷取 / 幀裁切對齊 / 色彩正規化。  
8. 格式輸出：序列幀 → Sprite Sheet（≤ 4096 寬），影片 → WebM VP9 CRF 28。  
9. 產生 manifest：包含 `id / type / duration / fps / atlasRect / pivot / memoryCost / preloadPhase`。  
10. 引擎整合：Cocos / Pixi / Phaser 動態載入測試 + 性能計數。  
11. QA：對照檢查清單（第 12 節）。  
12. 版本封存：`assets/animations/{category}/{id}/v{n}`。  
13. 發佈：更新 CDN / bundle，刷新快取索引。  

---
## 5. 規格資料結構 Contract（簡化）
```json
{
  "id": "symbol_win_lion_v1",
  "category": "symbolWin",
  "trigger": "payline_match",
  "resolution": "512x512",
  "fps": 30,
  "frames": 18,
  "durationSec": 0.6,
  "format": "spritesheet",
  "loops": false,
  "pivot": {"x": 0.5, "y": 0.5},
  "atlas": {"sheet": "symbols_win_a.png", "rect": [1024, 0, 512, 512]},
  "performanceBudgetKB": 420,
  "dependencies": ["fx_glow_gold"],
  "generated": {"model": "veo-3", "promptHash": "a91fbc..."},
  "qa": {"luminanceAvg": 0.72, "loopError": 0.0, "alphaIntegrity": 0.98}
}
```

---
## 6. Prompt Engineering 模板
通用核心：`主體 + 動作 + 相機 + 光線 + 材質/風格 + 氛圍 + 技術指示`

### 6.1 符號命中 (Symbol Win)
```
Generate a short slot symbol win animation.
Subject: {symbol_description}
Action: energetic burst, scale pulse subtle (8%), gold rune light sweep.
Camera: locked orthographic center.
Lighting: high contrast rim light + soft key, warm golden accents.
Style: stylized realism, crisp edges, saturated highlights.
Background: clean transparent or neutral dark for alpha extraction.
Timing: 0.6-0.8s @30fps, emphasis frames at 4, 10, 14.
Deliverable goal: consistent centroid, no motion crop, no trailing artifacts.
```
### 6.2 連線效果 (Line Win Overlay)
```
Create a translucent energy line traversal effect across slot paylines.
Visual: luminous flowing beam, slight particle embers, accent sparks at node intersections.
Camera: static, full frame 1920x1080.
Timing: 0.9-1.1s single pass.
Color: adaptive base color {payline_color}, additive glow.
Goal: dark-safe luminance (peak < 95%).
```
### 6.3 聽牌 (Near-Miss / Tease)
```
Generate a tension-building near-miss animation for a slot reel column.
Mood: anticipation + subtle dramatic light shift.
Action: symbol shimmer, ambient pulse, soft camera micro-zoom (≤3%).
Avoid: excessive flicker, disorienting shake.
Duration: 1.2s.
```
### 6.4 背景循環 (Loop Background)
```
Create a seamless atmospheric loop background.
Theme: {environment_theme}
Seamless loop: ensure first and last frame continuity via cyclical motion.
Motion intensity: low-medium; no distracting focal bursts.
Length: 6s @24fps.
```
### 6.5 Big Win / Mega Win 演出
```
Generate a celebratory big win cinematic.
Elements: central title emblem + radial golden light + coin burst layers + volumetric rays.
Camera: push-in slight (5%) over duration.
Duration: 2.5s.
Phasing: 0-0.5 buildup, 0.5-1.6 peak cascade, 1.6-2.5 settling shimmer.
```

---
## 7. Veo 3 生成策略
| 策略 | 說明 | 參數建議 |
|------|------|----------|
| 多變體生成 | 同一 Prompt + 不同種子 | seeds: 3–6 |
| 參數掃描 | 攝影運動幅度 / 光線對比 / 色飽和 | 每次改 1 維度 |
| 負面指令 | 避免 artifacts、過曝、motion blur smear | `avoid oversharpen, avoid clipping highlights` |
| 風格鎖定 | 使用 reference frame(s) | refStrength 0.3–0.55 |
| 迭代評估 | Gemini 比對語義 + brightness histogram | 亮度區間 0.1–0.92 |
| Loop 友善 | 描述循環性 (cyclical, seamless loop) | Prompt 顯式標記 |

---
## 8. 後處理管線（技術詳解）
1. 影片下載與驗證 → 解析度 / 時長 / FPS。  
2. Loop 修補：crossfade 6–12 帧 or optical-flow 重建。  
3. Alpha 擷取：背景移除 / matte 精修 (1px feather)。  
4. 幀抽取：`ffmpeg -i in.webm frame_%03d.png`。  
5. 幀裁切：bbox → 對齊中心點。  
6. Sprite Sheet 打包：`maxAtlasW=4096`，高度降序排布。  
7. 色彩規範：Lab ΔE < 4 vs baseline。  
8. 壓縮：zopflipng / CRF 20/24/28 選最優體積/質量平衡。  
9. 產 meta：pivot / frameRect / fps / trigger。  
10. 預覽頁：HTML + JS 播放 + 記憶體估算。  

---
## 9. 自動化腳本（偽代碼）
```python
from pipeline import gemini_plan, veo_generate, evaluate_clip, extract_frames, build_spritesheet

req = load_yaml('effects_catalog.yaml')
for eff in req['effects']:
    prompt = gemini_plan(eff)
    clips = veo_generate(prompt, variants=4)
    for c in clips:
        score = evaluate_clip(c, rules=eff['qaRules'])
        if score['pass']:
            frames = extract_frames(c)
            sheet = build_spritesheet(frames)
            save_assets(eff['id'], sheet, meta=score['metrics'])
            break
```

---
## 10. 資料夾與命名
```
assets/
  animations/
    symbol/win/lion/v1/lion_win_sheet.png
    line/line_generic_v1.webm
    background/base_loop_v2.webm
    transition/base_to_free_v1.webm
    bigwin/bigwin_standard_v3.webm
    result/result_panel_v1.webm
manifest/animation_manifest.json
```
模式：`<category>_<subtype?>_<identifier>_v<version>.<ext>`

---
## 11. 效能與封包預算
| 類別 | 單個上限 | 載入策略 | 降級方案 |
|------|----------|----------|----------|
| 符號命中 | 450 KB | 首次觸發快取 | 幀數 18→12 |
| Line Win | 300 KB | 預載 (高頻) | Glow 稀疏化 |
| Near-Miss | 380 KB | 條件預載 | 去粒子層 |
| Big Win | 1.2 MB | 延遲載入 | 金幣粒度減少 |
| 背景 Loop | 2.5 MB | 首屏載入 | 降 FPS / 提 CRF |
| Transition | 1.0 MB | 進入前預取 | 降運鏡幅度 |

---
## 12. QA 檢查清單
| 項目 | 標準 |
|------|------|
| 解析度 | 與規格匹配，無拉伸 |
| FPS | 偏差 ≤ 0.5fps |
| 亮度/對比 | RGB ≥ 250 區域 < 0.5% |
| Loop | Δ像素 RMS < 2.0 |
| Alpha | 無鋸齒 / 黑邊 / 暈染 |
| 中心穩定 | 漂移 ≤ 5% 寬 |
| 記憶體 | 符合預算 |
| 命名/版本 | meta 同步 |

---
## 13. 風險控管與回滾
| 風險 | 緩解 | 回滾 |
|------|------|------|
| Veo 產出不穩 | 多種子 + 閾值過濾 | 改用上版 v(n-1) |
| 風格漂移 | reference frame 套用 | 鎖定 style embedding 包 |
| 體積膨脹 | 報表預警 | 自動壓縮 batch |
| Loop 接縫 | crossfade/optical flow | 降級靜態背景 |
| 播放卡頓 | 預載策略 + 降 FPS | 提供低階包 |

---
## 14. 持續優化與數據回饋
1. 埋點：播放次數 / 中途取消 / 完整觀賞率。  
2. KPI：失敗率、平均迭代次數、平均體積。  
3. A/B：Big Win 兩版 → 留存 / 局時長。  
4. 體積閾值：> 預算 15% 自動排壓縮。  

---
## 15. Manifest 範例
```json
{
  "version": "2025.10.03-anim-v1",
  "generatedBy": "ai-pipeline-gemini-veo",
  "groups": {
    "preload": ["background/base_loop_v2"],
    "lazy": ["bigwin/bigwin_standard_v3", "transition/base_to_free_v1"],
    "onDemand": ["symbol/win/lion_v1"]
  },
  "assets": [
    {
      "id": "lion_symbol_win",
      "path": "animations/symbol/win/lion/v1/lion_win_sheet.png",
      "meta": "animations/symbol/win/lion/v1/lion_win_sheet.json",
      "memoryKB": 412,
      "preloadPhase": "onDemand"
    }
  ]
}
```

---
## ✅ 快速落地建議
1. 建立 `effects_catalog.yaml`（10 個核心動態）。
2. 腳本：Prompt 生成 → Veo API 呼叫 → 後處理。  
3. 先跑通「符號命中」類別端到端。  
4. 建立 KPI：平均迭代 / 體積 / QA 通過率。  
5. 週期回顧 → 調整 Prompt 模板與壓縮策略。  

---
## 16. 動態特效美術規格書定義（Art Spec for Dynamic FX）

本章提供「動態特效美術規格書」標準模板，供美術 / 技術美術 / VFX / AI Pipeline 在製作與審核時使用，確保所有動態資產輸入資訊一致，減少反覆溝通與錯誤生成。

### 16.1 目的與使用時機
| 場景 | 使用本規格 | 備註 |
|------|------------|------|
| 新玩法加入新特效 | ✅ | 於 Gameplay 原型確立後第一週完成 |
| 現有效果升級（視覺加強） | ✅ | 標記 `revisionType=enhance` |
| 資產體積優化重製 | ✅ | 附上現行體積/效能報告 |
| 快速試驗概念 | 可選 | 可填精簡版 Minimal Spec |

### 16.2 規格書欄位總覽
| 欄位 | 必填 | 說明 | 範例 |
|------|------|------|------|
| id | ✅ | 唯一識別（對應 pipeline / manifest） | `symbol_win_lion_v1` |
| displayName | ✅ | 人類可讀名稱 | Lion Symbol Win |
| category | ✅ | 參考第 1 節分類 | `symbolWin` |
| subType | 選 | Big / Mega / Ultra / Generic | `mega` |
| triggerEvent | ✅ | 遊戲事件 | `payline_match` |
| priority | ✅ | 播放優先序（0 高→5 低） | 2 |
| layering | ✅ | 多層播放順序 | `base, glow, particles` |
| cameraType | 選 | orthographic / perspective | orthographic |
| durationSec | ✅ | 目標時長 | 0.6 |
| fps | ✅ | 幀率 | 30 |
| loops | ✅ | 是否循環 | false |
| expectedFrames | 選 | 預估總幀數（供 spritesheet 預算） | 18 |
| safeZoneRatio | 選 | 主體需落於區域（寬或高百分比） | 0.85 |
| motionIntensity | ✅ | none/low/medium/high | medium |
| energyCurve | 選 | 節奏相位 | `build→peak→settle` |
| colorPalette | ✅ | 主色/輔色/強調 | `["#D8A531", "#5A2D10", "#FFD675"]` |
| luminanceRange | ✅ | 亮度範圍（0-1） | `[0.08,0.92]` |
| styleTags | ✅ | 風格標籤 | `["stylized realism","golden glow"]` |
| forbiddenTraits | 選 | 禁用元素 | `["overexposed","hard flicker"]` |
| semanticKeywords | ✅ | 核心語義（語義比對用） | `["lion","gold","burst"]` |
| variantCount | ✅ | 初次生成變體數 | 4 |
| perfBudgetKB | ✅ | 體積預算（壓縮後） | 450 |
| atlasTarget | 選 | 預計放入的 Atlas 名稱 | `symbols_win_a` |
| audioSyncPoints | 選 | 音效節點（相對時間） | `[0.00,0.18,0.42,0.55]` |
| kpiFocus | 選 | KPI 關注點 | `["attention","retention"]` |
| revisionType | 選 | new/enhance/optimize/fix | new |
| notes | 選 | 其他補充 | `需要金色粒子尾巴` |

### 16.3 YAML 規格書範本（完整版）
```yaml
id: symbol_win_lion_v1
displayName: Lion Symbol Win
category: symbolWin
triggerEvent: payline_match
priority: 2
layering: [base, glow, particles]
cameraType: orthographic
durationSec: 0.6
fps: 30
loops: false
expectedFrames: 18
safeZoneRatio: 0.85
motionIntensity: medium
energyCurve: [build, peak, settle]
colorPalette: ["#D8A531", "#5A2D10", "#FFD675"]
luminanceRange: [0.08, 0.92]
styleTags: ["stylized realism", "radiant gold", "sharp highlights"]
forbiddenTraits: ["overexposed", "strobing", "muddy contrast"]
semanticKeywords: ["lion", "gold", "burst"]
variantCount: 4
perfBudgetKB: 450
atlasTarget: symbols_win_a
audioSyncPoints: [0.00, 0.18, 0.42, 0.55]
kpiFocus: ["winEmphasis"]
revisionType: new
notes: "顯示階段 0.15s 出現符文掃光，0.42s 進入能量峰值"
```

### 16.4 簡化版 Minimal Spec（快速概念驗證用）
```yaml
id: bigwin_intro_test_v0
category: bigWin
durationSec: 2.5
fps: 30
loops: false
variantCount: 2
semanticKeywords: ["coins","gold","title"]
perfBudgetKB: 1200
styleTags: ["cinematic","warm"]
```

### 16.5 層次（Layering）建議標準化分類
| 層 | 說明 | 是否可禁用（低階裝置） | 降級策略 |
|----|------|-----------------------|----------|
| base | 主體基本動作 | ❌ | N/A |
| glow | 外發光/內發光脈衝 | ✅ | 降亮度頻率、改靜態 |
| particles | 粒子飛散/能量碎片 | ✅ | 降發射數、移除尾跡 |
| rays | 造型光束 / 體積光 | ✅ | 改為靜態疊圖 |
| overlay | 疊加紋理（noise/rune） | ✅ | 降解析度或關閉 |
| embellish | 裝飾性附加元素 | ✅ | 全部移除 |

### 16.6 時間結構（Timing Blocks）
| Block | 比例（參考） | 功能 | 評估指標 |
|-------|--------------|------|----------|
| build | 20–30% | 集中視覺注意 | 增長梯度是否平滑 |
| peak | 40–55% | 最強視覺衝擊 | 亮度/顏色對比達標 |
| settle | 15–25% | 緩和視覺張力 | 是否無突兀閃斷 |
| exit (可選) | 5–10% | 平滑結束/淡出 | 無殘影/殘亮 |

### 16.7 語義與技術對齊檢查表（供 Gemini 評估）
| 項目 | 檢查方法 | 允收條件 |
|------|----------|----------|
| 主題語義 | 文字描述比對 semanticKeywords | 覆蓋率 ≥ 70% |
| 色彩一致性 | 取樣主體區域色相偏差 | 主色 Hue 偏差 < 12° |
| 亮度峰值 | 幀亮度直方圖 | 峰值 ≤ luminanceRange[1]+0.03 |
| 結構穩定 | 主體邊界方框位移 | 中心漂移 ≤ 5% |
| 節奏節點 | audioSyncPoints 附近亮度/大小變化 | 每節點±0.05s 內有事件 |

### 16.8 與 Pipeline 的映射
| Spec 欄位 | Pipeline 使用階段 | 功能 |
|-----------|------------------|------|
| semanticKeywords | evaluate（語義比對） | Gemini 語義得分計算 |
| perfBudgetKB | evaluate / pack | 產出後大小檢測 |
| layering | manifest | 決定載入與可降級組件 |
| motionIntensity | plan | Prompt 內運動形容詞強度 |
| luminanceRange | evaluate | 亮度閾值檢測 |
| audioSyncPoints | （未來）特效/音效對齊器 | 自動節點標記 |
| variantCount | generate | 建立種子/多變體數量 |

### 16.9 舉例：Line Win 特效規格（擴展示例）
```yaml
id: line_win_generic_v1
displayName: Generic Line Win
category: lineWin
triggerEvent: line_payout
priority: 3
layering: [base, glow]
durationSec: 0.9
fps: 30
loops: false
motionIntensity: low
colorPalette: ["#53C2FF", "#0A2233", "#FFFFFF"]
luminanceRange: [0.10, 0.88]
styleTags: ["energetic", "clean"]
semanticKeywords: ["line","energy","pulse"]
variantCount: 3
perfBudgetKB: 300
safeZoneRatio: 1.0
notes: "需保留中心透明區避免遮擋符號" 
```

### 16.10 版本與追蹤
| 欄位 | 說明 | 範例 |
|------|------|------|
| versionTag | 與產出檔關聯 | `symbol_win_lion_v1` |
| changeLog | 文字描述 | `v1 → 初版 / v2 → 降光暈` |
| obsolete | 是否淘汰 | false |
| replacedBy | 被哪版替代 | `symbol_win_lion_v2` |

### 16.11 推薦工作流程（建立 → 審核 → 生產）
1. 初稿（美術）→ 填寫 YAML（完整版或簡化版）。  
2. TA 技術審核：欄位完整性 + 體積預估。  
3. AI Pipeline 標記可自動化欄位（semanticKeywords / variantCount / perfBudget 轉換成 internal config）。  
4. 產出 `effects_catalog.yaml` 匯總 → 進入自動流程。  
5. 回寫執行結果（通過/失敗指標）到 Spec（可追加 `lastRun:` 區塊）。  
6. 迭代優化：調整 styleTags / forbiddenTraits。  

### 16.12 Spec 與 Catalog 的關係
單一 Spec 可獨立存在，`effects_catalog.yaml` 是多個 Spec 的集合索引。建議：
```
specs/
  symbol_win_lion_v1.yaml
  line_win_generic_v1.yaml
  bigwin_standard_v1.yaml
effects_catalog.yaml   # 只列出 id 與引用路徑
```

---
（動態特效美術規格書章節完）

## 17. 引擎內動態 / Tween 系統描述資產產生方式 SOP

本章定義：利用「程式化動態（Tween / Timeline / Shader / 粒子）」在引擎內建構動畫，替代或輔助預渲染資產，降低體積並提升可參數化重用能力。

### 17.1 適用場景
| 類型 | 適合程式化 | 理由 |
|------|-----------|------|
| 符號 Idle 輕動態 | ✅ | 週期短、重複出現、多符號共用 |
| Line Win 掃線 | ✅ | 幾何規則、顏色可程式化 |
| Near-Miss 邊框提醒 | ✅ | 簡單亮度 / scale / tint |
| Big Win 核心爆發 | 部分 | 複雜粒子/光束仍預渲染；文字/數字程式化 |
| 背景深度視差 | ✅ | UV 移動 / 多層合成 |
| 高擬真光影 | ✗ | 需預渲染材質細節 |

### 17.2 決策流程
```
需求標記 → 視覺複雜度評分 (1~5) → 目標裝置性能 → 是否需要精準物理光/粒 → 若否 → 程式化
```

### 17.3 程式化動畫資產描述 DSL（YAML）
```yaml
id: symbol_win_lion_runtime_v1
bindTo: SYM_Lion
duration: 0.6
fps: 60
loop: false
tracks:
  - type: tween
    id: scalePulse
    target: root
    prop: scale
    kf:
      - { t: 0.00, v: 1.00, ease: cubicOut }
      - { t: 0.08, v: 1.08 }
      - { t: 0.20, v: 1.02 }
      - { t: 0.40, v: 1.06 }
      - { t: 0.60, v: 1.00 }
  - type: shader
    id: sweep
    target: mat.glow
    uniform: sweepPos
    kf: [{ t: 0.00, v: 0.0 }, { t: 0.35, v: 1.0 }, { t: 0.60, v: 1.2 }]
  - type: color
    id: tintFlash
    target: root
    prop: tint
    kf: [{ t:0.00,v:'#FFFFFF'},{ t:0.12,v:'#FFE8A8'},{ t:0.32,v:'#FFCF60'},{ t:0.60,v:'#FFFFFF'}]
events:
  - { t:0.18, name:sfx_hit }
  - { t:0.42, name:sfx_peak }
perf:
  maxInstances: 30
  warnMs: 3.0
flags:
  allowSkip: true
```

### 17.4 Track 類型與引擎對應
| DSL type | 引擎操作 (Cocos) | PixiJS 實作 | 效能備註 |
|----------|------------------|------------|----------|
| tween | cc.tween/node.update | gsap / 自製 ticker | 減少多屬性拆分 |
| color | node.color / material | sprite.tint | 轉線性色空間避免 banding |
| shader | material.setProperty | filter.uniform | 控制更新頻率 ≥16ms |
| particle | 粒子系統 playOnce | pixi-particles | 共用 emitter pool |
| event | callback/time gate | eventEmitter | 避免大量 closure |

### 17.5 播放控制 API 建議
```ts
class RuntimeAnimPlayer {
  load(spec: AnimSpec): void
  play(opts?: { speed?: number; reverse?: boolean }): void
  stop(reset?: boolean): void
  setProgress(p01: number): void
  on(evt: string, cb: (time: number) => void): void
  isPlaying(): boolean
}
```

### 17.6 效能預算指標
| 指標 | 目標 | 量測方式 |
|------|------|----------|
| CPU update | < 0.5ms / 10 active | Timeline 聚合 | 聚合批次插值 |
| GPU uniform 更新 | < 50/秒 | shader batch 計數 | 合併寫入 buffer |
| 粒子執行 | < 1 emitter / 目標 | 計數 | 預熱 + 循環 reuse |
| 物件配置 | 0 動態 GC 峰值 | memory snapshot | 預先池化 |

### 17.7 QA 程式化檢查（自動化）
| 項目 | 方法 | Pass 條件 |
|------|------|-----------|
| 時間長度 | 播放實測 delta | |Δ| ≤ 1 frame |
| 同步事件 | 比對 event t vs 規格 | 誤差 ≤ 0.05s |
| 中心穩定 | bbox center 差異 | 偏移 ≤ 5% |
| 亮度曲線 | shader param 採樣 | 峰值在指定區段 |

### 17.8 Hybrid 整合策略
1. 影片 / spritesheet 作為「主能量」層。  
2. 程式化補：scale / tint / shader sweep / coin count jump。  
3. manifest 擴充：`{"runtimeSpec":"runtime_specs/xxx.yaml"}`。  

### 17.9 Gemini 產生 DSL Prompt 範例
```
Given an effect spec:
id: symbol_win_lion_v1
styleTags: ["stylized realism","radiant"]
energyCurve: [build, peak, settle]
Generate a compact YAML runtime tween spec with tracks: scale pulse, glow sweep, tint flash. Provide keyframes time (0~duration) four decimals, no commentary.
```

### 17.10 版本迭代策略
| 變更類型 | 說明 | 回溯策略 |
|----------|------|----------|
| 參數微調 | easing / tint | 保留上一版 JSON snapshot |
| 結構變更 | track 增刪 | 增版本號 `_v2` |
| 性能優化 | 合併 track | 標記 changeLog |

---
（引擎內動態 / Tween 系統章節完）

（本檔完）

## 18. Spine / Hybrid 動畫整合 SOP（與 Gemini / Veo 流程銜接）

### 18.1 目的
建立統一流程：影片 / spritesheet（Veo 或 Gemini Video）+ Spine 程式化骨架 / Tween 動畫同時交付，支援後續版本疊代與 QA。

### 18.2 產物矩陣
| 類型 | 來源 | 用途 | 優點 | 缺點 |
|------|------|------|------|------|
| Video Loop | Veo 3 / Gemini | 高能量主特效 | 光影/粒子品質高 | 記憶體佔用 | 
| SpriteSheet | Gemini Image + ffmpeg 拆幀 | 中能量循環 | 較好壓縮 | 幀數固定 |
| Spine Procedural | Runtime Tween DSL | 補間、輕量 idle | CPU 輕、可參數化 | 複雜粒子較弱 |
| Hybrid Manifest | export_hybrid_manifest | 封裝交付 | 單一入口 | 需整合管理 | 

### 18.3 Hybrid Manifest 結構（範例）
```json
{
  "id": "symbol_lion_win_v1",
  "version": "1.0.0",
  "video": {"path": "animations/symbol_lion_core.webm", "fps": 30, "loop": true},
  "skeleton": {"path": "skeletons/symbol_lion_skeleton.json", "entry": "idle"},
  "runtimeSpec": "runtime_specs/symbol_lion_win.yaml",
  "sync": {"startOffset": 0.0, "eventAlign": [{"event": "peak", "videoTime": 1.267, "runtimeTime": 1.25}]},
  "perfBudget": {"gpuMs": 0.4, "memMB": 18},
  "hash": "<sha256-all-files>"
}
```

### 18.4 生成步驟 Pipeline 對照
| Stage | Video/Sprite | Spine | Runtime DSL | Artifact |
|-------|--------------|-------|-------------|----------|
| Plan  | Prompt (Veo) | 骨架推導 | DSL prompt | plans/*.yaml |
| Gen   | Veo/Gemini Video | ai_agent skeleton | DSL YAML | raw/* |
| Eval  | 迴圈誤差/亮度 | bone 完整性 | 指標合法 | eval/*.json |
| Post  | 去首尾抖動 | 名稱正規化 | 時間對齊 | post/* |
| Pack  | webm / sheet | skeleton.json | runtime.yaml | dist/* |
| Manifest | embed meta | embed meta | embed ref | manifest/*.json |

### 18.5 Gemini 角色
1. 視覺語意 → 骨架（部件、關節父子）
2. Prompt 製作 → Veo 影片敘述、否定詞精煉
3. 骨架 QA 建議（對稱性 / 過長鏈 / 缺 slot）
4. DSL 優化：自動建議 ease / peak 時序對齊影片亮度峰值

### 18.6 Veo 角色
1. 高能量 win / transition 主動畫
2. 提供光影 / volumetric / 粒子基礎層
3. 迭代：透過 Gemini 評估差異 prompt 調整

### 18.7 同步策略
1. 影片分析：HDR 亮度 curve → peak time
2. DSL track 中 peak 事件（或 scale 最大）與該時間對齊
3. 骨架 idle 與影片循環長度 LCM（最小公倍數）優化重合避免跳變

### 18.8 版本與 Hash
計算：`sha256(video) ^ sha256(skeleton) ^ sha256(runtimeSpec)` → manifest.hash。差異檢測：任一檔案 hash 改變即遞增 patch 版號。

### 18.9 QA 指標補充
| 指標 | 描述 | 工具 | 門檻 |
|------|------|------|------|
| loopSeamRMS | 首尾幀像素差 RMS | ffmpeg + numpy | < 2.5 |
| luminancePeakTime | 峰值時間 | 自動亮度掃描 | 與 DSL peak Δ<=0.06s |
| boneCoverage | slot 數 / 圖層數 | skeleton 分析 | ≥ 0.95 |
| runtimeKeyframes | 總補間關鍵數 | 解析 DSL | < 180 |

### 18.10 CLI 對應（目前已實作 / 規劃）
| 目的 | 指令 | 狀態 |
|------|------|------|
| 生成骨架 | generate_from_layers | 已實作 |
| 生成提示詞 | gen_prompt | 已實作 |
| Hybrid 打包 | export_hybrid_manifest | 已實作 |
| 骨架規格驗證 | validate_spec | 已實作 |
|（計畫）影片分析 | analyze_video_loop | TODO |
|（計畫）Hash + Manifest 更新 | build_manifest | TODO |

### 18.11 下一步落地優先序
1. 影片 loop 分析 + runtime peak 對齊
2. Hash / 版本自動遞增
3. DSL 解析器 + 後端實際播放模組
4. Web 預覽頁 (Pixi + spine-ts) 原型
5. Gemini 實接：prompt → skeleton JSON + 建議調整 diff

（Section 18 完）

