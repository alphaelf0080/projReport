@echo off
:: 檢查管理員權限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ================================================================
    echo 需要管理員權限
    echo ================================================================
    echo.
    echo 正在請求管理員權限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

chcp 65001 >nul
cls
echo ================================================================
echo 🔧 設定防火牆規則 - Concept Art Generator Backend
echo ================================================================
echo.

set PORT=3010
set RULE_NAME_IN=Concept Art Backend 3010 In
set RULE_NAME_OUT=Concept Art Backend 3010 Out

echo 📋 設定資訊：
echo    Port: %PORT%
echo    規則名稱: %RULE_NAME_IN%, %RULE_NAME_OUT%
echo.

:: 刪除舊規則
echo 🗑️  清理舊規則...
netsh advfirewall firewall delete rule name="%RULE_NAME_IN%" >nul 2>&1
netsh advfirewall firewall delete rule name="%RULE_NAME_OUT%" >nul 2>&1
netsh advfirewall firewall delete rule name="Concept Art Backend 3010" >nul 2>&1
echo ✅ 舊規則已清理
echo.

:: 添加輸入規則
echo ➕ 添加輸入規則（允許外部連入 port %PORT%）...
netsh advfirewall firewall add rule name="%RULE_NAME_IN%" dir=in action=allow protocol=TCP localport=%PORT% profile=any enable=yes
if %errorlevel% equ 0 (
    echo ✅ 輸入規則添加成功
) else (
    echo ❌ 輸入規則添加失敗
)
echo.

:: 添加輸出規則
echo ➕ 添加輸出規則（允許 port %PORT% 對外通訊）...
netsh advfirewall firewall add rule name="%RULE_NAME_OUT%" dir=out action=allow protocol=TCP localport=%PORT% profile=any enable=yes
if %errorlevel% equ 0 (
    echo ✅ 輸出規則添加成功
) else (
    echo ❌ 輸出規則添加失敗
)
echo.

:: 驗證規則
echo 🔍 驗證防火牆規則...
echo.
netsh advfirewall firewall show rule name="%RULE_NAME_IN%"
echo.

echo ================================================================
echo ✅ 防火牆設定完成！
echo ================================================================
echo.
echo 下一步：
echo 1. 啟動後端服務：python main_gemini.py
echo 2. 測試本機連線：curl http://localhost:%PORT%/api/health
echo 3. 測試遠端連線：在遠端主機執行上述命令（將 localhost 改為伺服器 IP）
echo.
echo 按任意鍵關閉視窗...
pause >nul
