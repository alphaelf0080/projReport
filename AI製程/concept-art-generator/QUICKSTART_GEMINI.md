# Gemini 版本快速啟動指南

## 🎯 系統特色

✅ **無需本地 GPU** - 使用 Google Gemini API  
✅ **對話式互動** - AI 主動引導收集需求  
✅ **智能 Prompt 生成** - 自動產出最佳化提示詞  
✅ **色板分析** - 自動提取參考圖顏色  
✅ **即時反饋** - 支援 WebSocket 即時對話  

---

## 📋 前置需求

### 1. Google Gemini API Key

前往 [Google AI Studio](https://makersuite.google.com/app/apikey) 申請免費 API Key

### 2. Python 環境

```bash
python3 --version  # 需要 3.8+
```

---

## 🚀 快速安裝（macOS/Linux）

### 步驟 1: 安裝依賴

```bash
cd backend
pip3 install -r requirements-gemini.txt
```

### 步驟 2: 設定 API Key

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案，填入您的 API Key
nano .env
```

在 `.env` 中設定：
```bash
GEMINI_API_KEY=你的_API_KEY
```

### 步驟 3: 啟動後端

```bash
python3 main_gemini.py
```

看到以下訊息表示成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Gemini Agent 初始化成功
```

### 步驟 4: 啟動前端

開啟新終端機：

```bash
cd ../frontend
python3 -m http.server 3000
```

### 步驟 5: 開啟瀏覽器

訪問：http://localhost:3000/index_gemini.html

---

## 💬 使用流程

### 1️⃣ 描述需求

與 AI 對話，例如：
```
我想做一個東方龍主題的 Slot Game，
風格要華麗、金碧輝煌，
主角是一條紅色的龍，
背景有金色雲彩
```

### 2️⃣ 上傳參考圖（可選）

- 拖曳圖片到上傳區
- AI 自動分析色板
- 根據色彩提供建議

### 3️⃣ 確認 Prompt

AI 會逐步引導並生成結構化 Prompt：
- 主題描述
- 風格標籤
- 構圖建議
- 光線設定
- 色彩方案

### 4️⃣ 生成圖像

點擊「開始生成」：
- 生成 4 張變體
- 不同角度/光線
- 16:9 比例適合 Slot Game

### 5️⃣ 迭代優化

根據結果繼續對話：
```
第 2 張不錯，但龍的細節可以更豐富，
加入更多金色鱗片
```

---

## 🔧 API 端點

### 對話
```bash
POST /api/chat
{
  "session_id": "optional-uuid",
  "message": "我想做東方龍主題"
}
```

### 上傳參考圖
```bash
POST /api/upload-reference?session_id=xxx
FormData: file
```

### 生成圖像
```bash
POST /api/generate
{
  "session_id": "uuid",
  "prompt": "...",
  "num_images": 4
}
```

### 查詢狀態
```bash
GET /api/generation/{generation_id}
```

### WebSocket 即時對話
```javascript
ws://localhost:8000/ws/chat/{session_id}
```

---

## 📊 對話範例

```
👤 使用者: 我想做一個維京主題的遊戲

🤖 AI: 很棒的主題！維京主題充滿史詩感。讓我了解更多細節：
      1. 視覺風格偏好：寫實、卡通化，還是帶有奇幻元素？
      2. 色調：冷峻的藍灰色系，還是溫暖的金黃色系？
      3. 主要場景：戰場、海上航行，還是北歐神殿？

👤 使用者: 寫實風格，冷峻的藍灰色，戰場場景

🤖 AI: 完美！我已經構思出以下方案：
      
      【主題】維京戰士史詩戰場
      【風格】寫實、電影級質感
      【色彩】冰藍、鐵灰、戰旗紅
      【構圖】英雄正面特寫，背景戰場
      【光線】暴風雨中的戲劇性側光
      
      ✅ Prompt 已準備就緒，可以開始生成了！
```

---

## 🛠️ 疑難排解

### 問題 1: Gemini Agent 未初始化

**症狀**: API 回應 503 錯誤

**解決**:
```bash
# 檢查 .env 是否存在
ls -la .env

# 確認 API Key 已設定
cat .env | grep GEMINI_API_KEY

# 重新啟動後端
python3 main_gemini.py
```

### 問題 2: 無法連線到後端

**症狀**: 前端顯示「後端連線失敗」

**解決**:
```bash
# 確認後端是否運行
curl http://localhost:8000/api/health

# 檢查防火牆設定
# 確認 8000 port 未被佔用
lsof -i :8000
```

### 問題 3: 圖像生成失敗

**症狀**: 顯示佔位符圖片

**原因**: Imagen API 未實作（需單獨申請）

**替代方案**:
1. 使用 Gemini 生成 Prompt
2. 複製到 Stable Diffusion WebUI
3. 或整合其他圖像生成 API（DALL-E、Midjourney等）

---

## 📈 進階設定

### 使用 WebSocket 即時對話

在 `app_gemini.js` 中取消註解：

```javascript
// 初始化時啟用 WebSocket
initWebSocket();
```

### 自訂 System Prompt

編輯 `backend/services/gemini_agent.py`:

```python
def _load_system_prompt(self) -> str:
    return """你是... (自訂提示詞)"""
```

### 整合其他圖像生成 API

編輯 `backend/services/gemini_agent.py` 的 `GeminiImageGenerator` 類別：

```python
async def generate(self, prompt: str, **kwargs):
    # 呼叫 Replicate、RunwayML 等 API
    # 或本地 Stable Diffusion API
    pass
```

---

## 🎨 最佳實踐

### 1. 分階段對話

**不要**:
```
做一個遊戲主視覺
```

**應該**:
```
我想做東方龍主題
→ 華麗金色風格
→ 電影打光
→ 16:9 寬螢幕比例
```

### 2. 使用參考圖

上傳 2-3 張參考圖：
- 色彩參考
- 構圖參考
- 風格參考

### 3. 具體描述

**模糊**: "好看的龍"
**具體**: "金色鱗片、紅色眼睛、盤旋在雲端的東方龍"

### 4. 迭代優化

每次對話聚焦一個改進點：
- ✅ "龍的細節再豐富一些"
- ✅ "背景雲彩加入金色光暈"
- ❌ "改成埃及主題" (應開新 Session)

---

## 📝 API Key 申請指南

### Google Gemini (免費)

1. 訪問 https://makersuite.google.com/app/apikey
2. 登入 Google 帳號
3. 點擊「Create API Key」
4. 複製 Key 到 `.env`

**額度**: 
- 免費版：60 請求/分鐘
- 足夠開發測試使用

### Imagen (圖像生成)

目前需要申請 Google Cloud 帳號並啟用 Imagen API（付費）

**替代方案**:
- Replicate (穩定、付費)
- Stability AI (官方 API)
- 本地 Stable Diffusion

---

## 🚀 生產部署

### 使用 Docker

```bash
# 待補充 Dockerfile
```

### 環境變數

生產環境建議設定：
```bash
DEBUG=false
ALLOWED_ORIGINS=https://yourdomain.com
RATE_LIMIT=100
```

---

## 📞 支援

遇到問題？
- 📖 查看完整文檔：`README.md`
- 🐛 回報問題：GitHub Issues
- 💬 社群討論：Discussions

---

**🎉 開始創作出色的 Slot Game Concept Art！**
