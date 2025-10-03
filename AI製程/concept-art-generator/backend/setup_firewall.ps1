# ================================================================
# Windows 防火牆設定腳本 - Concept Art Generator Backend
# 功能：開啟 port 3010，允許遠端連線
# 執行：需要管理員權限
# ================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🔧 設定防火牆規則 - Concept Art Generator Backend" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 檢查管理員權限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ 錯誤：此腳本需要管理員權限" -ForegroundColor Red
    Write-Host "請以「系統管理員身分執行」PowerShell，然後再執行此腳本" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按 Enter 鍵結束"
    exit 1
}

# 設定變數
$PORT = 3010
$RULE_NAME_IN = "Concept Art Backend 3010 In"
$RULE_NAME_OUT = "Concept Art Backend 3010 Out"

Write-Host "📋 設定資訊：" -ForegroundColor Green
Write-Host "   Port: $PORT" -ForegroundColor White
Write-Host "   規則名稱: $RULE_NAME_IN, $RULE_NAME_OUT" -ForegroundColor White
Write-Host ""

# 刪除舊規則（如果存在）
Write-Host "🗑️  清理舊規則..." -ForegroundColor Yellow
try {
    netsh advfirewall firewall delete rule name="$RULE_NAME_IN" 2>$null | Out-Null
    netsh advfirewall firewall delete rule name="$RULE_NAME_OUT" 2>$null | Out-Null
    netsh advfirewall firewall delete rule name="Concept Art Backend 3010" 2>$null | Out-Null
    Write-Host "✅ 舊規則已清理" -ForegroundColor Green
} catch {
    Write-Host "⚠️  沒有找到舊規則" -ForegroundColor Gray
}

Write-Host ""

# 添加輸入規則
Write-Host "➕ 添加輸入規則（允許外部連入 port $PORT）..." -ForegroundColor Yellow
$result = netsh advfirewall firewall add rule `
    name="$RULE_NAME_IN" `
    dir=in `
    action=allow `
    protocol=TCP `
    localport=$PORT `
    profile=any `
    enable=yes

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 輸入規則添加成功" -ForegroundColor Green
} else {
    Write-Host "❌ 輸入規則添加失敗" -ForegroundColor Red
}

Write-Host ""

# 添加輸出規則
Write-Host "➕ 添加輸出規則（允許 port $PORT 對外通訊）..." -ForegroundColor Yellow
$result = netsh advfirewall firewall add rule `
    name="$RULE_NAME_OUT" `
    dir=out `
    action=allow `
    protocol=TCP `
    localport=$PORT `
    profile=any `
    enable=yes

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 輸出規則添加成功" -ForegroundColor Green
} else {
    Write-Host "❌ 輸出規則添加失敗" -ForegroundColor Red
}

Write-Host ""

# 驗證規則
Write-Host "🔍 驗證防火牆規則..." -ForegroundColor Yellow
Write-Host ""
netsh advfirewall firewall show rule name="$RULE_NAME_IN"
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✅ 防火牆設定完成！" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 啟動後端服務：python main_gemini.py" -ForegroundColor White
Write-Host "2. 測試本機連線：curl http://localhost:$PORT/api/health" -ForegroundColor White
Write-Host "3. 測試遠端連線：在遠端主機執行上述命令（將 localhost 改為伺服器 IP）" -ForegroundColor White
Write-Host ""
Read-Host "按 Enter 鍵結束"
