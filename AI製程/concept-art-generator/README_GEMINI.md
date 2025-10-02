# 🎨 AI Slot Game Concept Art Generator - Gemini Edition

> 使用 **Google Gemini** 的對話式 Slot Game Concept Art 創作系統

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)](https://ai.google.dev/)

---

## ✨ 特色功能

### 🤖 AI 驅動對話
- **智能引導**: Gemini AI 主動詢問關鍵細節
- **需求收集**: 主題、風格、色彩、氛圍
- **Prompt 生成**: 自動產出結構化 AI 繪圖提示詞

### 🎨 美術工具
- **色板提取**: 從參考圖自動分析主色調
- **多變體生成**: 一次產出 4 張不同角度/光線圖像
- **迭代優化**: 根據反饋持續改進

### 💻 技術優勢
- **無需本地 GPU**: 使用 Google Gemini API
- **即時互動**: 支援 REST API 和 WebSocket
- **響應式 UI**: 支援桌面與移動裝置
- **完整文檔**: API 文檔自動生成

---

## 📋 系統架構

```
concept-art-generator/
├── backend/                    # FastAPI 後端
│   ├── main_gemini.py         # 主應用程式
│   ├── services/              # 核心服務
│   │   ├── gemini_agent.py    # Gemini 對話代理
│   │   └── palette_extractor.py # 色板提取
│   ├── models/                # 資料模型
│   │   └── schemas.py
│   ├── requirements-gemini.txt # 依賴清單
│   └── .env                   # 環境變數
│
├── frontend/                   # 前端介面
│   ├── index_gemini.html      # 主頁面
│   ├── app_gemini.js          # 前端邏輯
│   └── style.css              # 樣式
│
├── start_gemini.sh            # 快速啟動腳本
└── QUICKSTART_GEMINI.md       # 快速指南
```

---

## 🚀 快速開始

### 前置需求

- Python 3.8+
- Google Gemini API Key ([免費申請](https://makersuite.google.com/app/apikey))

### 安裝步驟

#### 1️⃣ 安裝依賴

```bash
cd backend
pip3 install -r requirements-gemini.txt
```

#### 2️⃣ 設定 API Key

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯並填入您的 API Key
nano .env
```

在 `.env` 中設定：
```bash
GEMINI_API_KEY=你的_GEMINI_API_KEY
```

#### 3️⃣ 啟動服務

**方法 A: 使用啟動腳本（推薦）**
```bash
./start_gemini.sh
```

**方法 B: 手動啟動**
```bash
# Terminal 1 - 後端
cd backend
python3 main_gemini.py

# Terminal 2 - 前端  
cd frontend
python3 -m http.server 3000
```

#### 4️⃣ 開啟瀏覽器

訪問: **http://localhost:3000/index_gemini.html**

---

## 💬 使用流程

### 對話示範

```
👤 您: 我想做一個東方龍主題的 Slot Game

🤖 AI: 很棒的主題！讓我了解更多細節：
      1. 視覺風格：寫實、華麗、還是簡約風格？
      2. 色彩偏好：金紅色系、藍綠色系？
      3. 龍的形象：威嚴霸氣、祥瑞溫和？

👤 您: 華麗寫實風格，金紅色系，威嚴霸氣的龍

🤖 AI: 完美！我已構思出以下方案：
      
      ✅ 主題：東方神龍降臨
      ✅ 風格：電影級寫實、金碧輝煌
      ✅ 色彩：crimson & golden
      ✅ 構圖：S型盤旋，黃金比例
      ✅ 光線：戲劇性側光 + 體積光
      
      Prompt 已準備就緒，可以開始生成了！
```

### 完整流程

1. **描述需求** - 與 AI 對話說明您的創作想法
2. **上傳參考圖** (可選) - AI 自動分析色板
3. **確認 Prompt** - AI 生成結構化提示詞
4. **生成圖像** - 點擊按鈕開始創作
5. **迭代優化** - 根據結果繼續對話改進

---

## 🔧 API 文檔

### 核心端點

#### 1. 對話端點

```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "optional-uuid",
  "message": "我想做東方龍主題",
  "context": {  // 可選
    "reference_palette": ["#D4AF37", "#8B0000"]
  }
}
```

**回應:**
```json
{
  "session_id": "uuid",
  "response": "AI 的回應內容",
  "prompt_ready": false,
  "prompt_data": null,
  "timestamp": "2025-01-02T10:30:00"
}
```

#### 2. 參考圖上傳

```http
POST /api/upload-reference?session_id=xxx
Content-Type: multipart/form-data

file: [圖片檔案]
```

**回應:**
```json
{
  "session_id": "uuid",
  "palette": {
    "colors": [
      {
        "hex": "#D4AF37",
        "name": "golden",
        "percentage": 0.35
      }
    ]
  },
  "message": "參考圖分析完成"
}
```

#### 3. 生成圖像

```http
POST /api/generate
Content-Type: application/json

{
  "session_id": "uuid",
  "prompt": "cinematic masterpiece...",
  "negative_prompt": "low quality...",
  "num_images": 4,
  "aspect_ratio": "16:9"
}
```

#### 4. 查詢生成狀態

```http
GET /api/generation/{generation_id}
```

**回應:**
```json
{
  "generation_id": "uuid",
  "status": "completed",  // "processing" | "completed" | "failed"
  "images": ["url1", "url2", "url3", "url4"],
  "progress": 100
}
```

#### 5. WebSocket 即時對話

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/{session_id}');

// 發送
ws.send(JSON.stringify({
  message: "你的訊息"
}));

// 接收
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.response);
};
```

---

## 📊 系統元件

### Backend 服務

#### GeminiConceptAgent
```python
from services.gemini_agent import GeminiConceptAgent

agent = GeminiConceptAgent(api_key="your_key")

# 對話
result = await agent.chat("我想做東方龍主題")

# 檢查 Prompt 是否準備好
if result['prompt_ready']:
    prompt_data = result['prompt_data']
    # {
    #   "theme": "東方神龍",
    #   "prompt": "完整提示詞",
    #   "style_tags": ["cinematic", "realistic"],
    #   ...
    # }
```

#### PaletteExtractor
```python
from services.palette_extractor import PaletteExtractor

extractor = PaletteExtractor()

# 從圖片提取色板
palette = extractor.extract_from_image("ref.jpg")

# 結果
# {
#   "colors": [
#     {"hex": "#D4AF37", "name": "golden", "percentage": 0.35},
#     {"hex": "#8B0000", "name": "crimson", "percentage": 0.25}
#   ],
#   "primary": ["#D4AF37"],
#   "secondary": ["#8B0000"],
#   "accent": ["#FFD700"]
# }
```

### Frontend 應用

```javascript
// 發送訊息
async function sendMessage() {
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      message: userMessage
    })
  });
  
  const data = await response.json();
  
  if (data.prompt_ready) {
    // 啟用生成按鈕
    enableGenerateButton(data.prompt_data);
  }
}

// 生成圖像
async function generateImages() {
  const response = await fetch('/api/generate', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      prompt: currentPromptData.prompt
    })
  });
  
  const { generation_id } = await response.json();
  
  // 輪詢狀態
  pollGenerationStatus(generation_id);
}
```

---

## 🛠️ 進階配置

### 自訂 System Prompt

編輯 `backend/services/gemini_agent.py`:

```python
def _load_system_prompt(self) -> str:
    return """你是一位專業的 Slot Game 美術總監...
    
    【角色定位】
    - 專精東方、西方、奇幻等多種主題
    - 精通 AI 繪圖工具的 Prompt 工程
    
    【核心任務】
    1. 需求收集
    2. Prompt 生成
    3. 互動優化
    
    ... (自訂內容)
    """
```

### 整合圖像生成 API

編輯 `backend/services/gemini_agent.py`:

```python
class GeminiImageGenerator:
    async def generate(self, prompt: str, **kwargs):
        # 選項 1: Replicate
        response = await replicate.run(
            "stability-ai/sdxl",
            input={"prompt": prompt}
        )
        
        # 選項 2: 本地 Stable Diffusion API
        response = requests.post(
            "http://localhost:7860/sdapi/v1/txt2img",
            json={"prompt": prompt}
        )
        
        # 選項 3: OpenAI DALL-E
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1
        )
        
        return image_urls
```

### 環境變數

```bash
# .env
GEMINI_API_KEY=your_key            # 必須
IMAGEN_API_KEY=your_key            # 可選（圖像生成）
DEBUG=true                          # 開發模式
PORT=8000                           # 後端端口
ALLOWED_ORIGINS=*                   # CORS 設定
RATE_LIMIT=100                      # API 速率限制
```

---

## 📈 性能優化

### 1. 使用 WebSocket

取消註解 `app_gemini.js` 中的:
```javascript
initWebSocket();
```

好處:
- 即時雙向通訊
- 減少 HTTP 請求
- 更快的回應時間

### 2. 快取機制

```python
# 在 gemini_agent.py 中添加
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_prompt_generation(theme, style):
    # 快取常用的 Prompt 組合
    pass
```

### 3. 批次生成

```python
# 一次生成多個變體
await image_generator.generate_batch([
    {"prompt": prompt1},
    {"prompt": prompt2},
    {"prompt": prompt3}
])
```

---

## 🐛 疑難排解

### 問題 1: Gemini API 錯誤

**症狀**: `503 Service Unavailable`

**解決方案**:
```bash
# 檢查 API Key
echo $GEMINI_API_KEY

# 測試 API 連線
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=$GEMINI_API_KEY"

# 確認配額
# 訪問: https://console.cloud.google.com/
```

### 問題 2: 無法連線後端

**症狀**: `ERR_CONNECTION_REFUSED`

**解決方案**:
```bash
# 檢查端口是否被佔用
lsof -i :8000

# 檢查防火牆
sudo pfctl -d  # macOS

# 檢查後端是否運行
curl http://localhost:8000/api/health
```

### 問題 3: 圖像生成失敗

**原因**: Imagen API 未實作（需單獨申請）

**替代方案**:
1. 使用 Gemini 生成 Prompt
2. 複製到其他 AI 繪圖工具:
   - Stable Diffusion WebUI
   - Midjourney Discord Bot
   - Leonardo.AI
   - Replicate API

---

## 📚 最佳實踐

### 1. 有效對話技巧

**❌ 不好的範例**:
```
"做一個好看的遊戲"
```

**✅ 好的範例**:
```
"我想做東方龍主題的 Slot Game，
風格要華麗寫實，
主色調是金色和紅色，
龍要盤旋在雲端，
氛圍要有神秘感和威嚴感"
```

### 2. 參考圖使用

- 上傳 2-3 張不同類型的參考圖
- 色彩參考、構圖參考、風格參考
- AI 會自動分析並融合元素

### 3. 迭代優化策略

每次對話聚焦一個改進點:
- ✅ "龍的鱗片細節再豐富"
- ✅ "背景雲彩加入金色光暈"
- ✅ "整體對比度提高 20%"
- ❌ "全部重做" (應開新 Session)

---

## 🎓 延伸閱讀

- [Google Gemini API 文檔](https://ai.google.dev/docs)
- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [Stable Diffusion Prompt 指南](https://prompthero.com/)
- [色彩理論基礎](https://www.interaction-design.org/literature/topics/color-theory)

---

## 📝 授權

MIT License - 詳見 [LICENSE](LICENSE)

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📞 聯絡方式

- 🐛 回報問題: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 討論: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 Email: your.email@example.com

---

**🎉 開始創作令人驚艷的 Slot Game Concept Art！**
