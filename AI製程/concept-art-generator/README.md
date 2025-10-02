# Slot Game Concept Art Generator - 互動式 AI 工具

## 專案概述
這是一個專為 Slot Game 美術人員設計的互動式 AI 工具，透過輸入主題、風格、色彩偏好和參考素材，快速生成高品質的 Concept Art。

## 功能特色
- 🎨 **引導式輸入**: 分步驟收集美術需求（主題/風格/色彩/參考）
- 🤖 **智能 Prompt 生成**: 自動組合最佳化的 AI 生成提示詞
- 🔄 **迭代優化**: 基於美術師反饋自動調整生成參數
- 📊 **色板管理**: 自動從參考圖提取色彩並應用
- 🎯 **風格一致性**: 確保多輪生成保持視覺統一
- 📝 **版本追蹤**: 完整記錄每次生成的參數與結果

## 系統架構
```
concept-art-generator/
├── backend/                 # FastAPI 後端
│   ├── main.py             # API 主程式
│   ├── models/             # 資料模型
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── token_weights.json  # Token 權重表
│   ├── services/           # 核心服務
│   │   ├── prompt_engine.py    # Prompt 組合引擎
│   │   ├── style_analyzer.py   # 風格分析器
│   │   ├── palette_extractor.py # 色板提取
│   │   └── image_generator.py  # 圖像生成
│   └── requirements.txt    # Python 依賴
├── frontend/               # 前端介面
│   ├── index.html         # 主頁面
│   ├── app.js             # 互動邏輯
│   └── style.css          # 樣式
├── output/                # 生成結果輸出
└── README.md
```

## 快速開始

### 1. 安裝依賴
```bash
cd backend
pip install -r requirements.txt
```

### 2. 啟動後端服務
```bash
python main.py
```
服務將在 `http://localhost:8000` 運行

### 3. 開啟前端介面
```bash
cd frontend
# 使用任何 HTTP 伺服器，例如：
python -m http.server 3000
```
前端將在 `http://localhost:3000` 運行

## API 端點

### POST /api/brief
建立新的創意簡報
```json
{
  "theme": "東方龍與財富",
  "styleKeywords": ["cinematic", "volumetric light", "golden accents"],
  "colorPreferences": {
    "primary": ["#B30012", "#D41F27"],
    "secondary": ["#CFA64D", "#F7E09A"]
  },
  "referenceUrls": ["https://example.com/ref1.jpg"]
}
```

### POST /api/generate
生成 Concept Art
```json
{
  "briefId": "brief_123",
  "count": 4,
  "ratio": "16:9"
}
```

### POST /api/feedback
提交美術師反饋
```json
{
  "generationId": "gen_456",
  "selections": ["img_b.png"],
  "ratings": {"img_b.png": 5},
  "adjustments": ["增強龍鱗立體感", "背景雲霧降低飽和度"]
}
```

### GET /api/generation/{gen_id}
查詢生成結果

## 使用流程

### 第 1 步：輸入創意簡報
在前端填寫表單：
- **主題**: 例如「東方龍與財富」
- **風格關鍵詞**: cinematic, volumetric light, ornate
- **色彩偏好**: 選擇主色和輔色
- **參考圖片**: 上傳或提供 URL

### 第 2 步：生成首批圖像
系統將生成 4-6 張風格框架（Style Frames），顯示不同的：
- 構圖角度（全景/中景/近景）
- 光線方向（頂光/側光/背光）
- 細節層次

### 第 3 步：提供反饋
- 選擇喜歡的圖像（可多選）
- 為每張圖打分（1-5 星）
- 標註問題（例：光線太平、背景太亂）
- 提出調整建議

### 第 4 步：迭代優化
系統根據反饋自動：
- 提高被選中圖像的 token 權重
- 插入補救性描述詞
- 調整構圖/光線參數
- 生成新一批改進版本

### 第 5 步：確定主視覺
重複步驟 3-4 直到滿意，最後：
- 選定 1-2 個主視覺方向
- 系統自動拆解可延伸元素
- 生成多比例版本（16:9, 4:5, 1:1）
- 輸出 PSD 分層檔案

## 技術說明

### Prompt 組合策略
系統使用分層結構組合 Prompt：
```
[風格層] + [主體層] + [構圖層] + [光線層] + [材質層] + [色彩層] + [技術參數]
```

範例：
```
Majestic oriental dragon coiling around luminous golden orb,
flowing auspicious clouds, cinematic composition, 
dramatic rim light, volumetric light rays,
intricate scales, ornate gold accents,
rich crimson and imperial gold palette,
premium slot game concept art, ultra detailed, 16:9
```

### Token 權重調整
```python
# 初始權重
{"volumetric light": 1.0, "dramatic rim light": 1.0}

# 使用者選擇包含此 token 的圖像後
{"volumetric light": 1.05, "dramatic rim light": 1.0}

# 使用者標註「光線太平」後
{"volumetric light": 1.1, "dramatic rim light": 1.15}  # 自動補償
```

### 回饋 → 調整映射表
| 反饋標籤 | 自動調整策略 |
|----------|--------------|
| "背景太搶" | 降低背景 token 權重，添加 `shallow depth of field` |
| "光線太平" | 添加 `dramatic rim light`, `high contrast lighting` |
| "細節過多" | 移除 `intricate`, `overly detailed`，改為 `clean` |
| "主體不突出" | 添加 `focal clarity`, `center emphasis` |
| "色彩混亂" | 限制 palette token，移除次要顏色詞 |

## 進階功能

### 色板自動提取
從參考圖中提取主色調：
```python
# 使用 k-means 聚類提取 6-8 個主色
# 透過 ΔE (色彩差異) 去除過於相似的顏色
# 輸出 HEX 色碼供 Prompt 使用
```

### 風格 Token 資料庫
內建常用風格語彙：
- **光線**: volumetric, rim light, god rays, soft ambient
- **材質**: metallic, ornate, intricate, glossy, matte
- **鏡頭**: cinematic, wide angle, close-up, dynamic angle
- **氣氛**: majestic, mysterious, energetic, serene

### 生成參數記錄
每次生成完整記錄：
```json
{
  "timestamp": "2025-10-02T10:30:00Z",
  "prompt": "完整 prompt...",
  "negativePrompt": "low quality, blurry...",
  "seed": 42118732,
  "model": "SDXL_base_1.0",
  "steps": 40,
  "cfg_scale": 7.0,
  "outputs": ["gen_001_a.png", "gen_001_b.png"]
}
```

## 配置與自訂

### 修改預設風格
編輯 `backend/models/token_weights.json`：
```json
{
  "cinematic": 1.0,
  "volumetric light": 1.0,
  "dramatic rim light": 0.8,
  "your_custom_token": 1.2
}
```

### 調整生成參數
在 `backend/services/image_generator.py` 中：
```python
DEFAULT_PARAMS = {
    "steps": 40,          # 推理步數 (20-50)
    "cfg_scale": 7.0,     # 提示詞影響力 (5-15)
    "width": 1024,        # 寬度
    "height": 576         # 高度 (16:9)
}
```

## 效能優化

### GPU 記憶體優化
```python
# 啟用 xformers 記憶體優化
pipe.enable_xformers_memory_efficient_attention()

# 使用 fp16 精度
pipe = pipe.to("cuda", dtype=torch.float16)
```

### 批次生成
一次生成多張變體以提高 GPU 利用率：
```python
images = pipe(
    prompt=[prompt] * 4,  # 批次 4 張
    num_inference_steps=40
).images
```

## 疑難排解

### Q: 生成速度太慢？
A: 
- 降低 `steps` 到 25-30
- 使用較小的解析度先預覽
- 考慮使用 LCM (Latent Consistency Model) 加速

### Q: 生成結果不穩定？
A:
- 增加 negative prompt 的限制
- 提高 cfg_scale 到 8-10
- 鎖定 seed 進行測試

### Q: 色彩不符預期？
A:
- 在 prompt 中明確指定色板
- 使用 ControlNet Color 約束
- 調整參考圖的權重

### Q: 風格漂移問題？
A:
- 鎖定 base model 版本
- 使用 LoRA 固定風格
- 提高風格 token 權重到 1.3+

## 未來擴充計畫

- [ ] **ControlNet 整合**: 支援 Pose/Depth/Canny 引導
- [ ] **LoRA 熱插拔**: 動態載入專案風格模型
- [ ] **元素自動裁切**: 使用 Saliency Map 拆解主視覺
- [ ] **Symbol 建議系統**: 從 KV 推薦可延伸的 Symbol 設計
- [ ] **A/B 測試框架**: 圖像偏好學習
- [ ] **多語言支援**: 中/英/日文界面

## 授權與致謝
- 本專案基於 Stable Diffusion XL
- 使用 FastAPI, diffusers, Pillow 等開源專案
- 設計參考業界 Slot Game 美術流程

## 聯絡資訊
- 專案維護: [待補充]
- 問題回報: [GitHub Issues]
- 文檔更新: 2025-10-02

---
**快速開始提示**：先執行後端，再開前端，首次啟動會下載模型（約 6GB），請確保網路暢通。
