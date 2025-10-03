@echo off
chcp 65001 >nul
echo ================================================================
echo 🚀 Concept Art Generator - 快速啟動與診斷
echo ================================================================
echo.

:menu
echo 請選擇操作：
echo.
echo [1] 🔧 設定防火牆（需要管理員權限）
echo [2] 🔍 診斷網路連線
echo [3] 🚀 啟動後端服務 (port 3010)
echo [4] 🌐 啟動前端服務 (port 3000)
echo [5] 🧪 測試後端連線
echo [6] 📝 顯示配置資訊
echo [0] ❌ 結束
echo.
set /p choice="請輸入選項 (0-6): "

if "%choice%"=="1" goto firewall
if "%choice%"=="2" goto diagnose
if "%choice%"=="3" goto start_backend
if "%choice%"=="4" goto start_frontend
if "%choice%"=="5" goto test_connection
if "%choice%"=="6" goto show_config
if "%choice%"=="0" goto end
goto menu

:firewall
echo.
echo ================================================================
echo 🔧 設定防火牆
echo ================================================================
echo.
echo 正在檢查管理員權限...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 錯誤：需要管理員權限
    echo 請以「系統管理員身分執行」此批次檔
    pause
    goto menu
)
echo ✅ 已確認管理員權限
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0setup_firewall.ps1"
pause
goto menu

:diagnose
echo.
echo ================================================================
echo 🔍 診斷網路連線
echo ================================================================
echo.
python "%~dp0diagnose_network.py"
pause
goto menu

:start_backend
echo.
echo ================================================================
echo 🚀 啟動後端服務
echo ================================================================
echo.
echo 正在啟動後端... (port 3010)
echo 提示：按 Ctrl+C 可停止服務
echo.
cd /d "%~dp0"
python main_gemini.py
pause
goto menu

:start_frontend
echo.
echo ================================================================
echo 🌐 啟動前端服務
echo ================================================================
echo.
echo 正在啟動前端... (port 3000)
echo 提示：按 Ctrl+C 可停止服務
echo.
cd /d "%~dp0..\frontend"
echo 前端目錄: %cd%
echo.
echo 啟動後請訪問:
echo   本機: http://localhost:3000/index_gemini.html
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        echo   區網: http://%%b:3000/index_gemini.html
    )
)
echo.
python -m http.server 3000
pause
goto menu

:test_connection
echo.
echo ================================================================
echo 🧪 測試後端連線
echo ================================================================
echo.

echo [1/3] 檢查 port 3010 是否開啟...
netstat -ano | findstr :3010
if %errorlevel% equ 0 (
    echo ✅ Port 3010 已開啟
) else (
    echo ❌ Port 3010 未開啟（後端可能未啟動）
)
echo.

echo [2/3] 測試本機連線...
curl -s http://localhost:3010/api/health
if %errorlevel% equ 0 (
    echo ✅ 本機連線成功
) else (
    echo ❌ 本機連線失敗
)
echo.

echo [3/3] 獲取本機 IP...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4" ^| findstr /v "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        echo 本機 IP: %%b
        echo.
        echo 測試 IP 連線...
        curl -s http://%%b:3010/api/health
        if errorlevel 1 (
            echo ❌ IP 連線失敗
        ) else (
            echo ✅ IP 連線成功
        )
    )
)
echo.
pause
goto menu

:show_config
echo.
echo ================================================================
echo 📝 當前配置資訊
echo ================================================================
echo.
echo 後端配置:
echo   Port: 3010
echo   Host: 0.0.0.0 (所有網路介面)
echo   檔案: main_gemini.py
echo.
echo 前端配置:
echo   Port: 3000
echo   檔案: frontend/index_gemini.html
echo.
echo 本機網路資訊:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    echo   %%a
)
echo.
echo API 端點:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4" ^| findstr /v "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        echo   本機訪問: http://localhost:3010
        echo   區網訪問: http://%%b:3010
        echo   健康檢查: http://%%b:3010/api/health
    )
)
echo.
echo 前端需要修改的配置 (frontend/app_gemini.js):
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4" ^| findstr /v "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        echo   const BACKEND_SERVER_IP = '%%b';
        echo   const BACKEND_PORT = 3010;
    )
)
echo.
pause
goto menu

:end
echo.
echo 感謝使用！
timeout /t 2 >nul
exit /b 0
