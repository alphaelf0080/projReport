# 🔧 遠端連線問題修正指南

## 📋 問題說明

遠端主機無法連接到後端服務 (port 3010)，出現 `TCP connect failed` 錯誤。

## ✅ 解決方案總結

已完成以下修正：

### 1. **後端配置** (`main_gemini.py`)
- ✅ 改用 port **3010** (原為 8000)
- ✅ 綁定到 `0.0.0.0` (允許所有網路介面連接)
- ✅ 添加網路資訊顯示（啟動時顯示本機 IP 和連接方式）

### 2. **前端配置** (`app_gemini.js`)
- ✅ 動態 API 配置（自動檢測本機或遠端訪問）
- ✅ 增強錯誤診斷訊息
- ✅ 添加詳細的連線狀態顯示

### 3. **工具腳本**
- ✅ `setup_firewall.ps1` - 自動設定 Windows 防火牆
- ✅ `diagnose_network.py` - 網路連線診斷工具
- ✅ `quick_start.bat` - 一鍵啟動和測試工具

---

## 🚀 快速修正步驟

### **步驟 1：設定防火牆（必須）**

**方法 A：使用腳本（推薦）**

1. 以**管理員身份**開啟 PowerShell
2. 執行：
   ```powershell
   cd c:\projects\projReport\AI製程\concept-art-generator\backend
   .\setup_firewall.ps1
   ```

**方法 B：手動執行命令**

以**管理員身份**執行 PowerShell：
```powershell
# 添加防火牆規則
netsh advfirewall firewall add rule name="Backend 3010 In" dir=in action=allow protocol=TCP localport=3010 profile=any

# 驗證規則
netsh advfirewall firewall show rule name="Backend 3010 In"
```

---

### **步驟 2：診斷網路狀態**

```bash
cd c:\projects\projReport\AI製程\concept-art-generator\backend
python diagnose_network.py
```

這會檢查：
- ✅ 本機 IP 地址
- ✅ Port 3010 是否開啟
- ✅ HTTP 連接是否正常
- ✅ 防火牆規則是否設定

---

### **步驟 3：啟動後端服務**

```bash
cd c:\projects\projReport\AI製程\concept-art-generator\backend
python main_gemini.py
```

**預期輸出：**
```
======================================================================
🚀 啟動 Gemini Concept Art Generator
======================================================================
主機名稱: YOUR-COMPUTER
本機 IP:  192.168.12.75
綁定介面: 0.0.0.0 (所有網路介面)
監聽端口: 3010
======================================================================
📍 本機訪問: http://localhost:3010
📍 區網訪問: http://192.168.12.75:3010
📍 健康檢查: http://192.168.12.75:3010/api/health
======================================================================
💡 遠端連線注意事項：
   1. 確認防火牆已開啟 port 3010
   2. 執行以下命令添加防火牆規則 (需管理員權限)：
      netsh advfirewall firewall add rule name="Backend 3010" dir=in action=allow protocol=TCP localport=3010
   3. 前端配置使用: http://192.168.12.75:3010
======================================================================
INFO:     Uvicorn running on http://0.0.0.0:3010 (Press CTRL+C to quit)
```

---

### **步驟 4：測試本機連接**

在**新的終端視窗**執行：

```bash
# 測試健康檢查端點
curl http://localhost:3010/api/health
```

**預期回應：**
```json
{
  "status": "healthy",
  "gemini_agent": true,
  "image_generator": true,
  "active_sessions": 0
}
```

---

### **步驟 5：測試遠端連接**

在**遠端主機**上執行：

```powershell
# 測試 TCP 連接
Test-NetConnection -ComputerName 192.168.12.75 -Port 3010

# 測試 HTTP 連接
curl http://192.168.12.75:3010/api/health
```

**預期輸出：**
```
TcpTestSucceeded : True
```

---

### **步驟 6：更新前端配置**

前端 `app_gemini.js` 已自動配置，但請確認 **BACKEND_SERVER_IP**：

```javascript
// 在 app_gemini.js 開頭
const BACKEND_SERVER_IP = '192.168.12.75';  // 👈 確認這是正確的 IP
const BACKEND_PORT = 3010;
```

---

### **步驟 7：啟動前端並測試**

```bash
cd c:\projects\projReport\AI製程\concept-art-generator\frontend
python -m http.server 3000
```

訪問：
- 本機：`http://localhost:3000/index_gemini.html`
- 遠端：`http://192.168.12.75:3000/index_gemini.html`

---

## 🛠️ 使用快速啟動工具

我們提供了一個整合工具，包含所有功能：

```bash
cd c:\projects\projReport\AI製程\concept-art-generator\backend
quick_start.bat
```

**功能選單：**
```
[1] 🔧 設定防火牆（需要管理員權限）
[2] 🔍 診斷網路連線
[3] 🚀 啟動後端服務 (port 3010)
[4] 🌐 啟動前端服務 (port 3000)
[5] 🧪 測試後端連線
[6] 📝 顯示配置資訊
[0] ❌ 結束
```

---

## 🔍 故障排除

### **問題 1：防火牆規則無效**

**症狀：** 遠端仍無法連接

**解決：**
1. 檢查規則是否真的生效：
   ```powershell
   netsh advfirewall firewall show rule name=all | findstr 3010
   ```

2. 檢查防火牆狀態：
   ```powershell
   Get-NetFirewallProfile | Select-Object Name, Enabled
   ```

3. 暫時關閉公用網路防火牆測試（僅診斷用）：
   ```powershell
   Set-NetFirewallProfile -Profile Public -Enabled False
   ```

4. 測試完後記得重新啟用：
   ```powershell
   Set-NetFirewallProfile -Profile Public -Enabled True
   ```

---

### **問題 2：Port 已被占用**

**症狀：** 啟動時出現 `Address already in use`

**解決：**
```powershell
# 查看誰占用了 port 3010
netstat -ano | findstr :3010

# 終止該程序（將 <PID> 替換為實際的 PID）
taskkill /PID <PID> /F
```

---

### **問題 3：後端綁定到錯誤的介面**

**症狀：** `netstat` 顯示 `127.0.0.1:3010` 而非 `0.0.0.0:3010`

**檢查：**
```powershell
netstat -ano | findstr :3010
```

**正確輸出應該是：**
```
TCP    0.0.0.0:3010           0.0.0.0:0              LISTENING       12345
```

**如果顯示 `127.0.0.1:3010`，檢查 `main_gemini.py` 的 `host` 參數是否為 `"0.0.0.0"`**

---

### **問題 4：IP 地址變更**

**症狀：** 電腦 IP 變了，前端連不上

**解決：**
1. 執行診斷工具確認新 IP：
   ```bash
   python diagnose_network.py
   ```

2. 更新前端配置：
   ```javascript
   const BACKEND_SERVER_IP = '新的IP地址';
   ```

---

## 📝 檢查清單

完成所有修正後，請確認：

- [ ] 防火牆規則已添加（port 3010）
- [ ] 後端在 port 3010 運行
- [ ] `netstat -ano | findstr :3010` 顯示 `0.0.0.0:3010`
- [ ] 本機可訪問 `http://localhost:3010/api/health`
- [ ] 本機可訪問 `http://192.168.12.75:3010/api/health`
- [ ] 前端 `BACKEND_SERVER_IP` 配置正確
- [ ] 遠端主機可 ping 通伺服器
- [ ] 遠端主機 `Test-NetConnection` 成功
- [ ] 遠端主機可訪問健康檢查端點
- [ ] 前端頁面狀態列顯示「✅ 已連線」

---

## 🎯 最終測試

**在伺服器上：**
```bash
# 1. 啟動後端
python main_gemini.py

# 2. 在新終端測試
curl http://localhost:3010/api/health
```

**在遠端主機上：**
```powershell
# 1. 測試連通性
Test-NetConnection -ComputerName 192.168.12.75 -Port 3010

# 2. 測試 API
curl http://192.168.12.75:3010/api/health

# 3. 瀏覽器訪問
# http://192.168.12.75:3000/index_gemini.html
```

---

## 📞 仍有問題？

如果完成以上所有步驟仍無法連接，請提供：

1. `diagnose_network.py` 的完整輸出
2. `netstat -ano | findstr :3010` 的結果
3. 防火牆規則列表：
   ```powershell
   netsh advfirewall firewall show rule name=all | findstr 3010
   ```
4. 遠端主機執行 `Test-NetConnection` 的完整輸出
5. 瀏覽器開發者工具 (F12) 的 Console 和 Network 標籤截圖

---

## ✅ 修正完成

現在您的系統應該：
- ✅ 後端在 port 3010 運行並接受外部連接
- ✅ 防火牆允許 port 3010 通訊
- ✅ 前端自動適配本機或遠端訪問
- ✅ 提供完整的診斷和測試工具

祝使用順利！🎉
