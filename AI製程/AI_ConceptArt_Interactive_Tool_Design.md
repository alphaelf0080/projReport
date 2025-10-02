# Slot Game Concept Art 互動式 AI Tool 設計方案

版本: 0.1.0  
日期: 2025-10-02  
目的: 協助美術人員輸入主題 / 風格 / 色彩偏好 / 參考素材 → 快速生成可迭代的 Slot Game Concept Art（主視覺 / Style Frames / 元素拆解）

---
## 1. 整體目標
建立一個「可對話 + 可迭代 + 可追蹤版本」的美術 AI 工作平台，結合文字 → 圖像 + 圖像 → 圖像 + 引導式 Prompt 組合，縮短概念階段並確保風格與後續符號/UI 生產可延展性。

### 1.1 成功判準 (Success Metrics)
| 指標 | 目標 | 說明 |
|------|------|------|
| 初稿生成時間 | < 3 分鐘 | 從輸入到首批 4–6 張 Style Frames |
| 風格一致性分數 | > 0.8 | 以 embedding 相似度衡量 (CLIP cosine) |
| 迭代接受率 | > 60% | 使用者選取保留的比例 |
| 可拆元素數量 | ≥ 6 | 後續可成為 Symbols 或 UI Icon 的元素 |

---
## 2. 系統架構概觀
```
+---------------- Frontend (Web) ---------------+
| Vue/React UI                                   |
|  - Input Wizard (主題/風格/色彩/參考上傳)       |
|  - 即時 Prompt 預覽                            |
|  - 生成任務進度 (WebSocket/EventSource)       |
|  - 圖像比較 / 投票 / 標記 / 批註              |
|  - Palette / Style Tokens 面板                |
+---------------------+--------------------------+
                      |
                (REST / WebSocket)
                      |
+------------------ Backend Orchestrator ------------------+
| FastAPI / Node (Python 建議 for Diffusers)               |
|  - Session & Brief Manager                               |
|  - Style Token Extractor                                 |
|  - Prompt Composer Service                               |
|  - Generation Job Dispatcher (Celery / RQ)               |
|  - Feedback Loop (Ranking Model / 加權重訓)              |
|  - Embedding Index (FAISS/Chroma)                        |
|  - Palette Extraction (k-means / histogram)              |
+------------------+------------------+--------------------+
                   |                  |
          +--------+-------+  +------+----------------+
          | Image Gen Core |  |  Reference Processing |
          |  - SD XL       |  |  - CLIP Tagging       |
          |  - LoRA 支援    |  |  - Similarity Search |
          |  - ControlNet  |  |  - Color Map Extract  |
          +--------+-------+  +-----------+-----------+
                   |                           |
             +-----+-----------+       +------+------+
             |  Storage (S3/MinIO)     |  DB (Postgres) |
             |  /raw /composed         |  sessions      |
             |  /thumb /lora_models    |  prompts       |
             |                         |  generations   |
             +-------------------------+  feedback      |
```

---
## 3. 關鍵模組職責
| 模組 | 功能 | 技術建議 |
|------|------|----------|
| Brief Manager | 整理輸入成標準化結構 | Pydantic Schema |
| Style Token Extractor | 從文字/參考圖抽取材質/光線/鏡頭語言 | LLM + CLIP + Keyword rule set |
| Palette Engine | 從參考圖聚類出主/輔/點綴色 | k-means (n=6~8) + ΔE 過濾 |
| Prompt Composer | 嵌入模板 → 組合 → 多變體策略 | Jinja2 / Rule-based weighting |
| Generation Engine | 產生風格圖 / Layer 拆分 | diffusers + ControlNet / IP-Adapter |
| Variation Manager | 針對焦點/背景/光線做條件變體 | Xformers + 子 prompt 權重 |
| Feedback Ranker | 依使用者選擇更新偏好模型 | ELO / Bradley-Terry / Weighted Voting |
| Asset Deriver | 從 KV 拆出可延伸元素裁切 | Edge detect + Saliency + 人工確認 |
| Version / Audit Logger | 紀錄每次 prompt / model hash / seed | DB + git-like hash |

---
## 4. 資料結構 (Schemas)
### 4.1 Brief Intake JSON
```json
{
  "projectId": "dragon_fortune_v1",
  "theme": "東方龍 財富 能量",
  "styleKeywords": ["cinematic", "volumetric light", "golden accents"],
  "colorPreferences": {
    "primary": ["#B30012", "#D41F27"],
    "secondary": ["#CFA64D", "#F7E09A"],
    "mood": "尊貴 能量 幸運"
  },
  "referenceImages": [
    {"id": "ref1", "url": "https://.../dragon_pose.png", "tags": []},
    {"id": "ref2", "url": "https://.../gold_lighting.jpg", "tags": []}
  ],
  "target": {"count": 6, "ratios": ["16:9", "4:5"], "detailLevel": "high"},
  "constraints": {"violence": false, "religiousSymbols": "avoid"}
}
```

### 4.2 Prompt Log Entry
```json
{
  "id": "gen_20251002_001",
  "briefId": "dragon_fortune_v1",
  "basePrompt": "Majestic oriental dragon ...",
  "negativePrompt": "low quality, blurry, watermark, disfigured, extra limbs",
  "styleTokens": ["luminous", "cinematic depth", "ornate gold"],
  "seed": 42118732,
  "model": {"name": "SDXL_base", "revision": "1.0", "loras": ["oriental_dragon_lora_v2"]},
  "control": [{"type": "pose", "strength": 0.5}],
  "outputIds": ["img_a.png", "img_b.png"],
  "createdAt": "2025-10-02T10:12:11Z"
}
```

### 4.3 Feedback Entry
```json
{
  "generationId": "gen_20251002_001",
  "userId": "artist_amy",
  "selections": ["img_b.png", "img_d.png"],
  "ratings": {"img_b.png": 5, "img_d.png": 4},
  "tags": {"img_b.png": ["good focal contrast"], "img_d.png": ["lighting too flat"]},
  "nextRequests": ["加強龍鱗立體感", "背景雲霧降低飽和度 20%"]
}
```

---
## 5. Prompt 組合策略
### 5.1 分層結構
```
[Preamble 風格層] + [主體語意層] + [構圖與鏡頭] + [光線與氣氛] + [材質/細節] + [色彩約束] + [用途標註] + [技術參數]
```

### 5.2 權重化示例 (適用 SD / MJ 類語法)
```
((Majestic oriental dragon:1.3)) coiling around ((luminous golden orb:1.2)), 
flowing auspicious clouds, volumetric light shafts, 
cinematic composition, rich crimson and imperial gold palette, 
intricate scales, radiant energy particles, ultra detailed, 16:9
```

### 5.3 負面提示詞模板
```
low quality, jpeg artifacts, watermark, oversaturated, mutated hands, extra limbs, distorted anatomy, noisy background, flat lighting, bland composition
```

### 5.4 動態調整（根據回饋）
| 回饋標籤 | 調整策略 |
|----------|----------|
| lighting too flat | +"dramatic rim light", +contrast token, seed jitter |
| focal unclear | +DOF 描述, 減少背景細節詞權重 |
| color clutter | 移除次要顏色詞 + 增加 palette 限定詞 |
| over-detailed | 降 low-level 細節詞權重 (intricate→detailed) |

---
## 6. 生成管線 (Pipeline)
| 步驟 | 描述 | 實作建議 |
|------|------|----------|
| 1. Brief Normalize | 清洗/拆詞/語意分類 | spaCy / jieba + LLM 摘要 |
| 2. Style Token 抽取 | 光線/材質/鏡頭語言標準化 | Token 庫 + 相似度匹配 |
| 3. Palette 擷取 | 參考圖聚類出 6 色 | k-means + ΔE 去重 |
| 4. Prompt 組裝 | 模板 + 權重 + 動態調整 | Jinja2 + 版本號 |
| 5. 生成任務入列 | 非同步處理 | Celery + Redis queue |
| 6. 圖像生成 | SD XL + (可選 IP-Adapter, ControlNet) | diffusers pipeline |
| 7. 品質預檢 | CLIP score / NSFW 過濾 | open_clip + safety checker |
| 8. Embedding 入庫 | 供檢索/相似比對 | ViT-L/14 embedding |
| 9. 回饋收集 | UI 評分/標籤 | REST / WebSocket |
| 10. 偏好更新 | Rank 模型調整 token 權重 | 存權重表 |

---
## 7. 回饋迭代 (Feedback Loop)
1. 收集「選擇 + 評分 + 說明」→ 權重表更新 (style_token_weight, negative_token_weight)。  
2. 若連續 2 輪「焦點不清」→ 自動加入 `shallow depth of field, focal clarity`。  
3. 生成版本差異對比：使用 SSIM + Embedding 距離產生「新意分值」。  
4. 保留最佳樣本作為下一輪的 img2img 引導 (strength 0.35~0.55)。

---
## 8. API 規劃 (FastAPI 示例)
```python
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class BriefIn(BaseModel):
    theme: str
    styleKeywords: List[str]
    colorPreferences: dict
    referenceUrls: List[str] = []
    target: dict

@app.post("/api/brief")
def create_brief(brief: BriefIn):
    # 1. normalize
    # 2. extract style tokens
    # 3. enqueue generation job
    return {"briefId": "brf_123", "status": "queued"}

@app.get("/api/generation/{gen_id}")
def get_generation(gen_id: str):
    # return status, thumbnails
    return {"id": gen_id, "status": "done", "images": ["/cdn/img_a.png"]}

class FeedbackIn(BaseModel):
    generationId: str
    selections: List[str]
    ratings: dict
    tags: Optional[dict] = None

@app.post("/api/feedback")
def submit_feedback(fb: FeedbackIn):
    # update token weights
    return {"ok": True}
```

---
## 9. 範例 Diffusers 生成片段 (Python)
```python
from diffusers import StableDiffusionXLPipeline
import torch, random

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
).to("cuda")

BASE_PROMPT = (
    "Majestic oriental dragon coiling around luminous golden orb, flowing auspicious clouds, "
    "cinematic composition, rich crimson and imperial gold palette, volumetric light rays, "
    "intricate scales, radiant energy particles, ultra detailed"
)
NEG = "low quality, watermark, blurry, distorted, extra limbs, flat lighting"

seed = random.randint(0, 2**32-1)
generator = torch.Generator(device="cuda").manual_seed(seed)

image = pipe(
    prompt=BASE_PROMPT,
    negative_prompt=NEG,
    num_inference_steps=40,
    guidance_scale=7.0,
    width=1024,
    height=576
).images[0]
image.save("kv_candidate.png")
```

---
## 10. 偏好模型 (簡易策略)
- 起始 token 權重 = 1.0  
- 被選中樣本中出現的 token → 權重 += 0.05  
- 被標籤為問題（ex: `lighting too flat`）→ 對應補救 token 插入列表  
- 連續三輪無選擇 → 觸發「發散模式」：增加構圖/光線隨機性 (seed shuffle + guidance_scale +-1)

權重表儲存範例：
```json
{
  "luminous": 1.15,
  "volumetric light": 1.1,
  "intricate": 0.95,
  "dramatic rim light": 1.05
}
```

---
## 11. 前端互動要點
| 功能 | UI 模式 | 備註 |
|------|---------|------|
| Brief Wizard | 分步 (主題→風格→色彩→參考) | 即時顯示 Prompt 預覽 |
| Reference 標記 | 拖曳上傳 + 自動標籤 + 人工修正 | CLIP tag + 編輯 |
| Palette 板 | 主/輔/點綴色塊 + HEX | 可一鍵鎖定不讓模型漂移 |
| 生成視圖 | Masonry + 批次多選 + 快速標籤 | 支援快捷鍵 (1-5 評分) |
| 差異檢視 | 選二圖 → SSIM/差異熱圖 overlay | 協助判斷迭代價值 |
| Prompt Diff | 顯示本輪與上一輪差異 highlight | 透明化過程 |
| Token 熱度 | 權重條形圖 | 可手動微調 |

---
## 12. 安全與合規
| 風險 | 防範 |
|------|------|
| 侵權風格仿冒 | 過濾輸入關鍵詞（如直接名畫家名） |
| 不適當內容 | NSFW / Violence classifier 過濾 |
| 文化敏感 | 建立禁用元素詞表（宗教符號錯用等） |
| 資料洩漏 | 圖片儲存加密、URL 有效期限制 |

---
## 13. 部署與基礎設施建議
| 元件 | 選項 | 備註 |
|------|------|------|
| Web 前端 | Vite + React / Vue3 | 快速開發 |
| API | FastAPI | Python 便於模型整合 |
| 任務隊列 | Redis + Celery | 可橫向擴充 |
| 模型推論 | A100/4090 GPU 節點 | 分離 service |
| 儲存 | MinIO (S3 相容) | 區分 raw / thumb / derived |
| DB | Postgres | JSONB 支援彈性欄位 |
| 向量索引 | Chroma / FAISS | 圖像相似度搜尋 |
| 監控 | Prometheus + Grafana | GPU/延遲/錯誤率 |

---
## 14. 演進路線 (Roadmap)
| 階段 | 功能 | 目標時間 |
|------|------|----------|
| Phase 1 | 基本 Brief → 批次生成 → 回饋儲存 | Week 2 |
| Phase 2 | Style Token & Palette 抽取 | Week 4 |
| Phase 3 | 迭代偏好權重 / Prompt Diff | Week 6 |
| Phase 4 | Layer 拆解 + Symbol Seed 建議 | Week 8 |
| Phase 5 | 自動化評分 (CLIP + 可讀性測試) | Week 10 |
| Phase 6 | A/B 圖像偏好學習模型 | Week 12 |

---
## 15. 快速啟動（最小可行原型）
1. 建立 FastAPI 專案 + `/api/brief` 與 `/api/generation/{id}`。  
2. 寫一個 Prompt 模板 + 固定 negative prompt。  
3. 用 diffusers 實作同步生成（先不做佇列）。  
4. 前端單頁：輸入主題/風格/色彩 → 顯示生成結果。  
5. 加入簡單 feedback (選擇喜歡的圖片) → 紀錄 JSON。  
6. 第二輪：調整 token 權重後再生成。

---
## 16. 可能的附加強化
- 支援 img2img：使用草圖 / 參考構圖引導。
- ControlNet Pose / Depth / Canny 多通道融合。
- LoRA 快速微調（30–60 張主題強化）。
- 自動產出「元素裁切」(saliency + contour)。
- 匯出一鍵生成 Branding Style Guide PDF。

---
## 17. 風險與對策
| 風險 | 描述 | 對策 |
|------|------|------|
| 生成不穩定 | 模型漂移導致風格跳動 | 鎖定 base model + 色板硬約束 |
| Artist 不信任 | 黑箱感 | Prompt Diff + 權重視覺化 |
| 延遲過高 | 大圖生成耗時 | 先低清→再 upscale 流程 |
| GPU 成本高 | 平均多輪迭代 | 設定配額 / 排程非尖峰 |

---
## 18. 後續可產出文件
- API 規格書 (OpenAPI YAML)
- 色板抽取演算法說明
- Prompt 權重調整策略白皮書
- 用戶操作手冊 (Wizard 流程圖)

---
**結語**: 以上方案可於 2–3 週內構建出 MVP。若需要我可再幫你：
1. 產生 FastAPI 專案骨架
2. 寫第一版 Prompt Composer 程式碼
3. 加入簡易前端表單樣板

請告訴我你想先執行哪一步。
