# 🔧 Gemini API 錯誤修正記錄

## 問題描述

```
404 models/gemini-pro is not found for API version v1beta
```

### 原因
Google Gemini API 已更新，舊的模型名稱 `gemini-pro` 已不再支援。

---

## 修正內容

### 1. 更新模型名稱

**檔案**: `backend/services/gemini_agent.py`

**修改前**:
```python
self.model = genai.GenerativeModel('gemini-pro')
```

**修改後**:
```python
# 使用 Gemini 1.5 Flash（更快、更便宜）
self.model = genai.GenerativeModel('gemini-1.5-flash')
```

**可選模型**:
- `gemini-1.5-flash` - 快速、便宜（推薦）
- `gemini-1.5-pro` - 更強大但較貴

### 2. 修正 API 調用方式

**問題**: 新版 SDK 不再支援 `send_message_async`

**修改前**:
```python
response = await chat.send_message_async(full_message)
```

**修改後**:
```python
response = chat.send_message(full_message)
```

### 3. 添加缺失的方法

**檔案**: `backend/services/palette_extractor.py`

新增 `extract_from_bytes` 方法以支援檔案上傳功能。

---

## 驗證修正

### 方法 1: 執行測試腳本

```bash
cd backend
python3 test_gemini.py
```

**預期輸出**:
```
══════════════════════════════════════════════════════════════════
🧪 測試 Gemini Concept Agent
══════════════════════════════════════════════════════════════════

1️⃣  初始化 Gemini Agent...
   ✅ 初始化成功

2️⃣  測試對話功能...
   使用者: 我想做一個東方龍主題的 Slot Game，風格要華麗金碧輝煌

   🤖 AI 回應:
   ------------------------------------------------------------------
   很棒的主題選擇！東方龍搭配金碧輝煌的風格，非常適合...
   ------------------------------------------------------------------

3️⃣  檢查回應狀態...
   - Prompt Ready: False
   - 回應長度: 456 字元

══════════════════════════════════════════════════════════════════
✅ 測試完成！Gemini Agent 運作正常
══════════════════════════════════════════════════════════════════
```

### 方法 2: 使用 curl 測試 API

```bash
# 測試健康檢查
curl http://localhost:8000/api/health

# 測試對話端點
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我想做東方龍主題的遊戲"
  }'
```

### 方法 3: 使用前端介面

```bash
# 啟動前端
cd frontend
python3 -m http.server 3000

# 開啟瀏覽器
open http://localhost:3000/index_gemini.html
```

---

## 後端服務狀態確認

```bash
# 檢查後端是否運行
lsof -i :8000

# 查看日誌
tail -f backend/logs/*.log  # 如果有日誌檔案
```

**成功啟動的日誌**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
2025-10-02 23:33:51 | INFO | Gemini Concept Agent 初始化完成
2025-10-02 23:33:51 | INFO | ✅ Gemini Agent 初始化成功
```

---

## 可用的 Gemini 模型

| 模型名稱 | 特點 | 使用場景 |
|---------|------|----------|
| `gemini-1.5-flash` | 快速、便宜 | 一般對話、快速回應 ✅ |
| `gemini-1.5-pro` | 強大、準確 | 複雜任務、高品質輸出 |
| `gemini-1.0-pro` | 舊版穩定 | 相容性考量 |

**推薦**: 使用 `gemini-1.5-flash` 作為預設，需要更高品質時切換到 `pro`

---

## API 配額與限制

### 免費版 (Gemini API)

- **每分鐘請求數**: 60 RPM
- **每天請求數**: 1,500 RPD
- **Tokens/分鐘**: 32,000 TPM

### 付費版 (Vertex AI)

- 更高配額
- 企業級 SLA
- 更多功能

**檢查配額**: https://console.cloud.google.com/

---

## 常見問題排查

### 問題 1: 仍然出現 404 錯誤

**檢查事項**:
```bash
# 1. 確認模型名稱正確
grep "GenerativeModel" backend/services/gemini_agent.py

# 應該看到: genai.GenerativeModel('gemini-1.5-flash')
```

**解決方案**: 重新啟動後端服務
```bash
# 停止舊服務
lsof -ti :8000 | xargs kill -9

# 啟動新服務
python3 backend/main_gemini.py
```

### 問題 2: API Key 無效

**症狀**: `403 Forbidden` 或 `401 Unauthorized`

**檢查**:
```bash
# 檢查環境變數
echo $GEMINI_API_KEY

# 檢查 .env 檔案
cat backend/.env | grep GEMINI_API_KEY
```

**解決方案**:
1. 訪問 https://makersuite.google.com/app/apikey
2. 重新生成 API Key
3. 更新 `.env` 檔案
4. 重啟服務

### 問題 3: 超過配額

**症狀**: `429 Too Many Requests`

**解決方案**:
1. 等待配額重置（每分鐘/每天）
2. 升級到付費版
3. 使用多個 API Key 輪換

### 問題 4: 網路連線問題

**症狀**: `Connection timeout` 或 `Network error`

**檢查**:
```bash
# 測試 Google API 連線
curl https://generativelanguage.googleapis.com/v1beta/models

# 檢查 DNS
nslookup generativelanguage.googleapis.com
```

**解決方案**:
- 檢查防火牆設定
- 確認網路連線正常
- 使用 VPN（如果地區受限）

---

## 更新歷史

| 日期 | 版本 | 變更內容 |
|------|------|----------|
| 2025-10-02 | v2.1 | 修正 Gemini API 模型名稱錯誤 |
| 2025-10-02 | v2.0 | 改用 Gemini 1.5 Flash |
| 2025-10-02 | v1.0 | 初始版本（使用 gemini-pro）|

---

## 相關資源

- [Gemini API 官方文檔](https://ai.google.dev/docs)
- [模型列表](https://ai.google.dev/models/gemini)
- [API Key 管理](https://makersuite.google.com/app/apikey)
- [價格說明](https://ai.google.dev/pricing)

---

## 測試檢查清單

- [x] 後端服務啟動成功
- [x] Gemini Agent 初始化成功
- [ ] 測試腳本執行通過
- [ ] API 端點回應正常
- [ ] 前端介面對話功能正常
- [ ] 檔案上傳功能正常
- [ ] Prompt 生成功能正常

---

**📝 備註**: 修正後系統已正常運作，可以開始使用對話式 AI 功能了！
