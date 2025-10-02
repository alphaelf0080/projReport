# AI Agent 輔助 Slot Game 美術素材開發 SOP

## 文件資訊
- **版本**: 1.1.0
- **建立日期**: 2025年10月2日
- **適用範圍**: Slot Game 美術素材快速生成
- **核心目標**: 透過 AI Agent 互動式協作，提升美術素材產出效率與品質

---

## 1. 專案啟動階段

### 1.1 需求收集與分析
**執行人員**: 美術總監 / 專案經理

#### 互動流程：
```
👤 執行人員 → 🤖 AI Agent
輸入：遊戲主題概念

AI Agent 回應：
- 分析主題特性
- 提供視覺風格建議
- 詢問詳細需求
```

#### 必要資訊清單：
- [ ] 遊戲主題（例：埃及、海盜、魔幻、東方等）
- [ ] 目標平台（Mobile / Desktop / Both）
- [ ] 解析度需求（標準：1920x1080 或自訂）
- [ ] 美術風格（寫實、卡通、像素、手繪等）
- [ ] 色調偏好（明亮、暗黑、繽紛等）
- [ ] 參考遊戲或素材範例

#### AI Agent 輔助指令範例：
```
"我需要開發一款[主題]風格的 Slot Game，
目標平台是[平台]，
希望美術風格偏向[風格描述]，
請幫我：
1. 分析這個主題的視覺元素特點
2. 建議符號（Symbol）設計方向
3. 提供色彩配置建議
4. 列出需要準備的素材清單"
```

---

## 2. 素材規劃階段

### 2.1 素材清單生成
**執行人員**: 主美 / 2D 美術師

#### AI Agent 互動步驟：

**步驟 1: 生成完整素材清單**
```
👤 "根據[遊戲主題]，生成完整的 Slot Game 素材清單，
包含：
- 遊戲符號（高、中、低價值）
- 特殊符號（Wild、Scatter、Bonus）
- 背景元素
- UI 元件
- 特效動畫需求"

🤖 AI Agent 輸出：
- 結構化素材清單（JSON/表格格式）
- 每個素材的尺寸建議
- 優先級標記
- 預估工作量
```

**步驟 2: 設計規格確認**
```
👤 "請為[具體素材項目]提供詳細設計規格"

🤖 AI Agent 提供：
- 推薦尺寸（含出血區）
- 圖層結構建議
- 命名規範
- 匯出格式要求
```

### 2.2 素材優先級排序
**執行人員**: 專案經理 / 主美

#### 互動範本：
```
👤 "根據開發時程，請幫我排列素材製作優先順序，
專案週期為[N週]，團隊規模[N人]"

🤖 AI Agent 輸出：
Phase 1 (Week 1-2): 核心遊戲符號
Phase 2 (Week 3): 特殊符號與背景
Phase 3 (Week 4): UI 與特效
Phase 4 (Week 5): 優化與 Polish
```

---

## 3. 素材生成階段

### 3.1 AI 圖像生成（初稿）
**執行人員**: 2D 美術師

#### 工具選擇建議：
- **Midjourney**: 高品質概念設計
- **DALL-E 3**: 精準度控制
- **Stable Diffusion**: 本地化控制與客製化
- **Adobe Firefly**: 商用授權安全

#### AI Agent 協助生成 Prompt：

**範例互動 1: Symbol 圖標生成**
```
👤 "我需要為[埃及主題] Slot Game 設計高價值符號，
包含：法老王、埃及豔后、金字塔"

🤖 AI Agent 生成 Prompt：
"A majestic Pharaoh portrait, golden headdress, 
detailed hieroglyphics, vibrant colors, 
slot game symbol style, transparent background, 
centered composition, 512x512px, 
--style elaborate --quality high"

並提供：
- 3-5 種 Prompt 變化版本
- 不同風格指導詞
- 負面提示詞建議
```

**範例互動 2: 背景場景生成**
```
👤 "需要一個[海盜船艙]背景，
要求：景深效果，支持符號清晰顯示"

🤖 AI Agent 建議：
Prompt: "Pirate ship interior background, 
wooden deck, treasure chests, 
soft depth of field, muted colors, 
optimized for game UI overlay, 
1920x1080px, cinematic lighting"

技術要點：
- 背景飽和度降低 30%
- 中央區域對比度調整
- 預留符號展示空間
```

### 3.2 AI 生成內容篩選
**執行人員**: 主美 / 美術總監

#### 評估標準：
- [ ] 符合遊戲主題風格
- [ ] 視覺清晰度（在小尺寸下可辨識）
- [ ] 色彩協調性
- [ ] 文化適宜性
- [ ] 技術可行性（是否易於動畫化）

#### AI Agent 輔助評估：
```
👤 "請評估這[N張]生成圖片，
根據 Slot Game 符號設計標準"

🤖 AI Agent 分析：
圖片 A: ⭐⭐⭐⭐⭐
- 優點：構圖清晰、色彩鮮明
- 缺點：細節過多，需簡化
- 建議：移除背景裝飾元素

圖片 B: ⭐⭐⭐
- 優點：風格統一
- 缺點：對比度不足
- 建議：增強邊緣對比
```

### 3.3 專業軟體精修
**執行人員**: 資深 2D 美術師

#### AI Agent 提供修改指引：

**Photoshop 工作流程：**
```
👤 "我要在 Photoshop 中優化這個[寶石符號]，
有什麼建議的步驟？"

🤖 AI Agent 輸出：
步驟 1: 去背處理
- 使用 Select Subject + Refine Edge
- 建議羽化值：0.5px

步驟 2: 色彩調整
- Curves: 提升高光區
- Hue/Saturation: 飽和度 +15

步驟 3: 細節強化
- Smart Sharpen (Amount: 80%, Radius: 1.0)
- 添加外發光效果（Glow: 2px, Opacity: 30%）

步驟 4: 圖層結構
建議圖層命名：
📁 [Symbol_Name]_Master
  ├─ Base_Color
  ├─ Highlights
  ├─ Shadows
  ├─ Effects_Glow
  └─ Outline
```

**Illustrator 向量化：**
```
👤 "需要將這個圖標轉為向量格式"

🤖 AI Agent 指導：
1. Image Trace 設定：
   - Mode: High Fidelity Photo
   - Colors: 32
   - Paths: 85%
   - Corners: 75%

2. Expand 後清理：
   - 移除小於 5px 的路徑
   - 合併相似色彩 (Tolerance: 5)

3. 最佳化輸出：
   - 格式：SVG / EPS
   - 尺寸：可縮放向量
```

### 3.4 主視覺 (Key Visual) 與 Concept Art AI 代理工作流
**階段定位**: 介於「1.需求 → 2.素材規劃」與「3.素材生成」之間的橋接層，用於確立整體視覺語言，驅動後續符號/背景/UI 風格一致。

#### 目標產出
- 高解析主視覺（1920x1080 / 2560x1440 / 市場宣傳 3000+ 寬）
- 3–5 張 Style Frames（風格錨點）
- 色彩與光影語言板（Color & Lighting Bible）
- 元素結構圖（可拆解 Layer 設計）
- Symbol 衍生種子清單（後續量產引用）

#### AI 代理角色分工
| 角色 | 功能 | 輸入 | 輸出 |
|------|------|------|------|
| BriefAgent | 解析創意簡報 | 主題/市場/受眾 | 視覺線索矩陣 | 
| MoodboardAgent | 建議參考方向 | 關鍵詞 | 圖像描述/參考分類 |
| StyleAgent | 收斂風格 | moodboard 選擇 | 風格語法（筆觸/材質/光線）|
| CompositionAgent | 組合構圖 | 風格 + 元素清單 | 版面配置 (Layout Grid) |
| PaletteAgent | 建立色板 | 主題意象詞 | 主次/警示/中性色表 |
| QAAgent | 品質審核 | 候選 KV/frames | 指標評分 + 修正建議 |

#### 全流程 10 階段
1. Brief Consolidation（簡報蒐集）
2. 語意概念圖譜（Semantic Map）
3. Moodboard 方向探索（散→收 3 輪）
4. Style Tokens 定義（材質/光線/鏡頭語言）
5. Style Frames 生成（AI 圖生圖/文生圖迭代）
6. 構圖格線與視覺階層（Focal Hierarchy）
7. 主視覺合成（局部最佳片段拼接→重生成→人工精修）
8. Layer 拆解與資產化（FG/Mid/BG/FX）
9. 延伸資產規劃（Symbol Seed Mapping）
10. QA 指標評估 & 凍結版本（Freeze）

#### 互動腳本示範
【Brief 壓縮】
```
"主題=東方龍與財富、受眾=25-45、情緒=尊貴/能量/幸運，請整理：主題核心/情緒光線元素/可用象徵物/需避免。"
```
【Moodboard 指令生成】
```
"用文字生成 6 組 Moodboard 方向：每組=主題形容+色調+材質詞+Midjourney 語法。"
```
【Style Frames Prompt 初版】
```
"Majestic oriental dragon coiling around luminous golden orb, flowing auspicious clouds, cinematic composition, crimson + imperial gold, volumetric light, premium slot game key visual, 16:9, ultra detailed --stylize 700 --quality 2"
```
【變體要求】
```
"產出 5 變體：光線角度/鏡頭距離（全景/中景/近景/仰角/俯視）不同，保留色彩核心。"
```

#### Layer 拆解建議
| Layer | 功能 | 技術建議 |
|-------|------|-----------|
| FX_Glow | 能量光暈 | Additive，可做序列特效 |
| FG_Subject | 主體（龍頭） | 高細節保留 RAW | 
| Mid_Energy | 能量環/火焰 | 拆分迴圈幀 |
| Mid_Treasure | 金幣堆疊 | 可程式散佈 |
| BG_Atmos | 雲霧/體積光 | 降解析度 + 模糊 |

#### QA 指標
| 指標 | 說明 | 門檻 |
|------|------|------|
| Readability@25% | 25% 縮放仍辨識焦點 | 盲測 ≥80% 指出主體 |
| Focal Contrast Ratio | 主體/背景亮度比 | ≥1.35 |
| Color Harmony | 主/副色 ΔE | < 18 |
| Derivation Seeds | 可拆元素數 | ≥6 |
| Variation Consistency | 5 次重生主題一致 | ≥4 |

#### 規格 JSON 範例
```json
{
  "focalPoint": "dragon_head_glow_orb",
  "ratios": ["16:9", "4:5", "1:1"],
  "layers": ["FX_Glow", "Dragon_Core", "Energy_Rings", "Treasure", "Atmos"]
}
```

#### Prompt 範本
| 類型 | 範本 |
|------|------|
| KV 主題 | "[主題] cinematic key visual, [主體描述], dynamic light arcs, premium slot art, 16:9, high dynamic range" |
| 近景細節 | "Close-up [元素] dramatic rim light, luxurious texture, shallow depth, 4k concept art" |
| 特效元素 | "Swirling golden energy ring, particle glow, transparent, VFX element" |

#### 常見問題修正
| 問題 | 指令 | 策略 |
|------|------|------|
| 焦點分散 | "降低背景亮點 30%" | 對比重分配 |
| 色彩雜訊 | "統一金色光源色溫 5200K" | 統一光源溫度 |
| 細節糊散 | "提升龍鱗局部清晰度 半徑1.2" | 區域銳化 |

#### 交付清單
- 多比例輸出 (16:9 / 4:5 / 1:1)
- Grey scale 對比版
- 色板（Hex + 使用場景）
- Layer PSD + 命名規範
- 衍生資產種子（≥6）
- Prompt log (版本化)

> 建議建立 `concept/` 目錄：`concept/moodboard/`, `concept/style_frames/`, `concept/key_visual/`, `prompt_log.md`。

---

## 4. 動畫與特效階段

### 4.1 動畫需求分析
**執行人員**: 動畫師 / 特效師

#### AI Agent 輔助規劃：
```
👤 "請為[金幣符號]設計勝利動畫，
時長約 1-2 秒"

🤖 AI Agent 提案：
動畫方案 A: 旋轉閃光
- Frame 1-10: 360度旋轉 (Ease-out)
- Frame 11-15: 放大 1.2x + 光暈效果
- Frame 16-20: 回彈至原大小 (Bounce)

動畫方案 B: 跳躍慶祝
- Frame 1-8: 向上跳躍
- Frame 9-12: 空中旋轉
- Frame 13-20: 彈性著地

技術實現：
- Spine 骨架動畫
- 或 Sprite Sheet (20 frames, 100x100px each)
```

### 4.2 特效素材生成
**執行人員**: VFX 美術師

#### AI 輔助生成粒子效果：
```
👤 "需要一個[星星閃爍]粒子特效，
用於符號消除動畫"

🤖 AI Agent 規劃：
Particle System 參數：
- 粒子數量：15-25
- 生命週期：0.5-1.0s
- 初速度：200-400 px/s
- 顏色漸變：#FFD700 → #FFFFFF → Alpha 0
- 縮放：1.0 → 0.2

素材需求：
- 星星圖片：32x32px, PNG with Alpha
- Glow 圖片：64x64px, Radial gradient

提供 After Effects 表達式：
wiggle(3, 50) // 添加隨機擺動
```

---

## 5. 技術整合階段

### 5.1 素材匯出規範
**執行人員**: 技術美術 / 2D 美術師

#### AI Agent 生成匯出檢查清單：
```
👤 "請提供 Cocos Creator 的素材匯出規範"

🤖 AI Agent 輸出：
✅ 匯出檢查清單：

符號素材 (Symbols):
- 格式：PNG-24 with Alpha
- 尺寸：256x256px (含 10% padding)
- 命名：sym_[類型]_[名稱]_[變體].png
  例：sym_high_pharaoh_01.png
- DPI：72 (網頁標準)
- 色彩空間：sRGB

背景素材 (Backgrounds):
- 格式：JPG (Quality 90) 或 WebP
- 尺寸：1920x1080px
- 命名：bg_[場景]_[層級].jpg
  例：bg_main_layer01.jpg

UI 元素 (UI Elements):
- 格式：PNG-24
- 多尺寸支援：@1x, @2x, @3x
- 9-slice 標記（如需拉伸）

動畫素材：
- Sprite Sheet: 2048x2048 (POT)
- JSON 描述檔案（對應格式）
- 或 Spine/DragonBones 專用格式
```

### 5.2 素材優化
**執行人員**: 技術美術

#### AI Agent 優化建議：
```
👤 "如何優化這批素材的檔案大小？
目前總大小 50MB，目標壓縮至 20MB"

🤖 AI Agent 分析與建議：

自動化壓縮工具：
1. TinyPNG API (PNG 壓縮 60-70%)
2. ImageOptim (批次無損優化)
3. WebP 轉換（減少 25-35% 大小）

具體策略：
📊 資產類型分析：
- Symbols (25MB) → WebP 轉換 → 預估 10MB
- Backgrounds (15MB) → 降解析度 + JPG → 預估 6MB
- UI Elements (10MB) → TinyPNG → 預估 4MB

提供自動化腳本：
[Python/Shell 腳本生成...]
```

---

## 6. 品質檢查階段

### 6.1 視覺一致性檢查
**執行人員**: 主美 / QA

#### AI Agent 輔助審查：
```
👤 "請檢查這組符號的視覺一致性"
[上傳 10 個符號圖片]

🤖 AI Agent 分析報告：
✅ 通過項目：
- 色彩風格統一
- 尺寸比例一致
- 邊緣處理相同

⚠️ 需調整項目：
- Symbol_03: 亮度偏低 (-15%)
- Symbol_07: 飽和度過高 (+20%)
- Symbol_09: 線條粗細不一致

建議調整參數：
Symbol_03: Brightness +15, Contrast +5
Symbol_07: Saturation -20
Symbol_09: 重新描邊（3px uniform stroke）
```

### 6.2 技術規格驗證
**執行人員**: 技術美術 / 開發工程師

#### AI Agent 自動檢測：
```
👤 "請驗證素材資料夾是否符合技術規範"
[指定資料夾路徑]

🤖 AI Agent 檢測結果：
📁 素材檢測報告：

✅ 通過 (85 files):
- 命名規範正確
- 尺寸符合要求
- 格式正確

❌ 錯誤 (5 files):
1. sym_wild.png 
   → 尺寸：300x280 (應為 256x256)
   
2. bg_main.png 
   → 格式應為 JPG
   
3. ui_btn-start.png 
   → 命名含非法字符 '-'

⚠️ 警告 (3 files):
- effect_glow.png: 檔案過大 (2.5MB)
  建議：壓縮至 < 500KB
```

---

## 7. 迭代優化階段

### 7.1 反饋收集與分析
**執行人員**: 專案經理 / 測試團隊

#### AI Agent 協助整理反饋：
```
👤 "整理這週的美術反饋並提供改進建議"
[輸入原始反饋內容]

🤖 AI Agent 結構化輸出：
📋 反饋分類報告：

高優先級 (立即處理):
1. 符號辨識度問題
   - 反饋："寶石符號在小螢幕難以區分"
   - 建議：增加邊緣對比 +30%，添加色彩編碼
   - 工作量：2 人天
   
中優先級 (本週完成):
2. 背景亮度調整
   - 反饋："背景過亮影響符號閱讀"
   - 建議：降低背景飽和度 -25%，添加暗角
   - 工作量：0.5 人天

低優先級 (下版本):
3. 動畫流暢度優化
   - 反饋："跳躍動畫略顯生硬"
   - 建議：增加中間幀，調整 easing 曲線
   - 工作量：1 人天
```

### 7.2 A/B 測試支援
**執行人員**: 數據分析師 / 美術團隊

#### AI Agent 輔助生成變體：
```
👤 "為[主 UI 按鈕]生成 3 種設計變體，
用於 A/B 測試"

🤖 AI Agent 提案：
變體 A (當前版本):
- 風格：扁平化
- 色彩：#FF6B35 (橙色)
- 形狀：圓角矩形

變體 B (高對比):
- 風格：新擬物化
- 色彩：#4ECDC4 (青色)
- 形狀：膠囊形
- 特色：內陰影 + 外發光

變體 C (經典款):
- 風格：金屬質感
- 色彩：金色漸層
- 形狀：斜角矩形
- 特色：高光反射效果

測試指標建議：
- 點擊率 (CTR)
- 平均互動時間
- 用戶偏好調查
```

---

## 8. 文檔與交付階段

### 8.1 設計文檔生成
**執行人員**: 主美 / 技術美術

#### AI Agent 自動生成文檔：
```
👤 "生成這個專案的美術設計文檔"

🤖 AI Agent 輸出：
📄 [遊戲名稱] 美術設計規範文檔

目錄：
1. 專案概述
2. 視覺風格指南
   - 色彩板
   - 字體規範
   - 視覺元素庫
3. 素材清單與規格
   [自動生成表格]
4. 動畫與特效規範
5. 技術限制與優化
6. 版本紀錄

格式：
- Markdown (開發團隊)
- PDF (客戶交付)
- 互動式 HTML (內部參考)
```

### 8.2 素材打包與交付
**執行人員**: 技術美術

#### AI Agent 輔助整理：
```
👤 "請協助組織最終交付的素材結構"

🤖 AI Agent 生成資料夾結構：
📦 [ProjectName]_Art_Assets_v1.0/
├─ 📁 01_Symbols/
│  ├─ High_Value/
│  ├─ Medium_Value/
│  ├─ Low_Value/
│  └─ Special/
├─ 📁 02_Backgrounds/
│  ├─ Main_Game/
│  ├─ Feature_Screens/
│  └─ Sources_PSD/
├─ 📁 03_UI/
│  ├─ Buttons/
│  ├─ Windows/
│  ├─ Icons/
│  └─ @2x, @3x/
├─ 📁 04_Animations/
│  ├─ Sprite_Sheets/
│  ├─ Spine_Assets/
│  └─ Preview_Videos/
├─ 📁 05_Effects/
│  └─ Particles/
├─ 📄 README.md
├─ 📄 Asset_Manifest.json
└─ 📄 Design_Spec.pdf

並生成檢查清單腳本
```

---

## 9. 工具與資源整合

### 9.1 推薦 AI 工具鏈

#### 圖像生成：
- **Midjourney** (概念設計)
- **DALL-E 3** (精準生成)
- **Stable Diffusion** (本地控制)
- **Adobe Firefly** (商用安全)

#### 圖像編輯：
- **Photoshop + AI Plugins**
  - Generative Fill
  - Remove Background
- **Remove.bg** (去背)
- **Topaz Gigapixel AI** (升頻)

#### 動畫與特效：
- **Runway ML** (AI 動畫生成)
- **EbSynth** (風格化動畫)
- **After Effects + AI Plugins**

#### 優化與處理：
- **TinyPNG** (壓縮)
- **ImageOptim** (優化)
- **Squoosh** (格式轉換)

### 9.2 AI Agent 整合建議

#### 推薦 AI 助手：
- **ChatGPT/Claude** (流程規劃、文檔生成)
- **Midjourney Bot** (圖像生成)
- **GitHub Copilot** (腳本自動化)
- **Custom GPTs** (專案特化 Agent)

#### 自訂 AI Agent 工作流：
```yaml
Agent 配置範例：
name: "SlotGameArtAssistant"
role: "美術製作專家"
capabilities:
  - prompt_engineering
  - asset_analysis
  - technical_specification
  - quality_assurance
knowledge_base:
  - slot_game_design_patterns
  - color_theory
  - animation_principles
  - technical_constraints
```

---

## 10. 最佳實踐與注意事項

### 10.1 AI 生成內容的法律考量
- ✅ 使用有商用授權的 AI 工具
- ✅ 對 AI 生成內容進行二次創作
- ✅ 保留所有生成紀錄與修改歷程
- ⚠️ 避免直接使用受版權保護的參考圖
- ⚠️ 確認生成內容的文化適宜性

### 10.2 人機協作平衡
- **AI 負責**: 初稿生成、重複性任務、數據分析
- **人類負責**: 創意方向、質量把關、細節優化
- **共同協作**: 迭代改進、風格統一、問題解決

### 10.3 效率提升指標
| 階段 | 傳統流程 | AI 輔助流程 | 效率提升 |
|------|----------|-------------|----------|
| 概念設計 | 3-5 天 | 0.5-1 天 | 70-80% |
| 素材初稿 | 10-15 天 | 3-5 天 | 60-70% |
| 迭代修改 | 5-7 天 | 2-3 天 | 50-60% |
| 技術整合 | 2-3 天 | 1 天 | 50% |
| **總計** | **20-30 天** | **6.5-10 天** | **65-70%** |

### 10.4 品質控制檢查點
- ✓ 每個階段結束前進行 AI 輔助審查
- ✓ 保持人工最終審核機制
- ✓ 建立標準化評分體系
- ✓ 收集並分析歷史數據優化流程

---

## 11. 快速參考

### 11.1 常用 AI Prompt 模板

#### 符號設計：
```
"Create a [主題] themed slot game symbol 
representing [概念], 
[風格描述], 
high quality, centered composition, 
transparent background, 512x512px"
```

#### 背景場景：
```
"[場景描述] background for slot game, 
[風格], 
muted colors, soft focus, 
optimized for UI overlay, 
1920x1080px, [光線描述]"
```

#### 特效元素：
```
"[特效類型] VFX element, 
[色彩], 
particle effect, 
transparent background, 
suitable for game animation, 
256x256px"
```

### 11.2 問題排查指南

| 問題 | AI 輔助診斷指令 | 解決方向 |
|------|-----------------|----------|
| 風格不統一 | "分析這組素材的視覺一致性" | 色彩/濾鏡統一 |
| 檔案過大 | "建議壓縮策略" | 格式轉換/優化 |
| 動畫卡頓 | "分析幀率與優化方向" | 減少幀數/簡化 |
| 符號難辨識 | "評估小尺寸可讀性" | 增強對比/簡化 |

---

## 12. 版本更新記錄

| 版本 | 日期 | 更新內容 | 負責人 |
|------|------|----------|--------|
| 1.0.0 | 2025-10-02 | 初版建立 | AI Agent Team |
| 1.1.0 | 2025-10-02 | 新增 3.4 主視覺與 Concept Art AI 工作流 | AI Agent Team |
| | | | |

---

## 附錄

### A. AI 工具訂閱費用參考
- Midjourney: $30-60/月
- ChatGPT Plus: $20/月
- Adobe Firefly: 包含於 Creative Cloud
- Runway ML: $15-95/月

### B. 學習資源
- [Midjourney 官方文檔](https://docs.midjourney.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Slot Game Design Patterns](需補充)

### C. 聯絡與支援
- 技術支援：[待補充]
- 流程諮詢：[待補充]

---

**文檔結束**

*本 SOP 為動態文件，隨著 AI 技術發展持續更新*
