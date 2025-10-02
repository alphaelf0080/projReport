# 快速啟動指南

## 第一次使用

### 1. 安裝依賴
```bash
cd backend
pip install -r requirements.txt
```

### 2. 啟動後端（Terminal 1）
```bash
cd backend
python main.py
```
後端將在 http://localhost:8000 運行

### 3. 啟動前端（Terminal 2）
```bash
cd frontend
python -m http.server 3000
```
前端將在 http://localhost:3000 運行

### 4. 開始使用
在瀏覽器開啟 http://localhost:3000

---

## 使用流程

### 步驟 1: 建立創意簡報
填寫以下資訊：
- **主題**: 例如「東方龍與財富」
- **風格關鍵詞**: cinematic, volumetric light, ornate
- **色彩**: 主色和輔色的 HEX 碼
- **參考圖**: 可選，提供圖片 URL

### 步驟 2: 生成圖像
- 點擊「開始生成」
- 等待 AI 處理（約 1-2 分鐘）
- 系統會生成 4-6 張風格框架

### 步驟 3: 評估與反饋
- 查看生成的圖像
- 選擇喜歡的圖像
- 為每張圖打分（1-5 星）
- 提供調整建議
- 提交反饋後重新生成

### 步驟 4: 迭代優化
重複步驟 2-3 直到滿意

---

## 測試範例

### 範例 1: 東方龍主題
```
主題: 東方龍與財富
風格: cinematic, volumetric light, golden accents
主色: #B30012, #D41F27
輔色: #CFA64D, #F7E09A
```

### 範例 2: 埃及法老
```
主題: 古埃及法老與金字塔
風格: dramatic lighting, ornate, mystical
主色: #C4A544, #8B4513
輔色: #4169E1, #DAA520
```

### 範例 3: 海盜寶藏
```
主題: 海盜船長與寶藏
風格: cinematic, dramatic rim light, weathered
主色: #8B4513, #CD7F32
輔色: #FFD700, #2F4F4F
```

---

## 常見問題

### Q: 首次啟動很慢？
A: 首次會下載約 6GB 的 SDXL 模型，請耐心等待。

### Q: 生成速度太慢？
A: 
- 確保使用 GPU (CUDA)
- 降低生成數量
- 減少推理步數（在 `image_generator.py` 中修改）

### Q: 記憶體不足？
A: 
- 關閉其他應用程式
- 降低批次大小
- 使用較小的圖像尺寸

### Q: 圖像風格不穩定？
A: 
- 提供更多參考圖
- 增加風格關鍵詞的權重
- 多次迭代並提供反饋

---

## 進階配置

### 調整生成參數
編輯 `backend/services/image_generator.py`:
```python
self.default_params = {
    "num_inference_steps": 40,  # 20-50
    "guidance_scale": 7.0,      # 5-15
    "width": 1024,
    "height": 576
}
```

### 修改 Token 權重
編輯 `backend/models/token_weights.json`

### 啟用 xformers 優化
需要 CUDA，可減少 GPU 記憶體使用約 30%

---

## 系統需求

### 最低需求
- Python 3.8+
- 8GB RAM
- 20GB 硬碟空間

### 建議配置
- Python 3.10+
- NVIDIA GPU (8GB+ VRAM)
- 16GB+ RAM
- 30GB 硬碟空間

---

## 故障排除

### 後端無法啟動
```bash
# 檢查依賴
pip list

# 重新安裝
pip install -r requirements.txt --force-reinstall
```

### 前端無法連接
檢查 CORS 設定和後端是否運行

### GPU 無法使用
```bash
# 檢查 CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 快速測試

使用 API 文檔測試：
1. 開啟 http://localhost:8000/docs
2. 測試 `/api/brief` 端點
3. 測試 `/api/generate` 端點
4. 查看 `/api/generation/{id}` 結果

---

## 聯絡支援
- 查看 README.md 獲取更多資訊
- 問題回報: [待補充]
