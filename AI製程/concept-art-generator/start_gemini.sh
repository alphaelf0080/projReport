#!/bin/bash
# Gemini 版本快速啟動腳本

echo "═══════════════════════════════════════════════════════════════"
echo "🎨 Slot Game Concept Art Generator - Gemini Edition"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 檢查 .env 檔案
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到 .env 檔案"
    echo ""
    echo "正在創建 .env 檔案..."
    cp backend/.env.example backend/.env
    echo ""
    echo "✅ 已創建 backend/.env"
    echo ""
    echo "📝 請編輯 backend/.env 並設定您的 GEMINI_API_KEY："
    echo "   nano backend/.env"
    echo ""
    echo "   或直接執行："
    echo "   export GEMINI_API_KEY='your_api_key_here'"
    echo ""
    read -p "按 Enter 鍵繼續（確認已設定 API Key）..."
fi

# 啟動後端
echo ""
echo "🚀 啟動後端服務..."
echo "──────────────────────────────────────────────────────────────"
cd backend

# 載入環境變數
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 啟動 FastAPI
python3 main_gemini.py &
BACKEND_PID=$!

echo "✅ 後端服務已啟動 (PID: $BACKEND_PID)"
echo "   URL: http://localhost:8000"
echo "   API 文檔: http://localhost:8000/docs"
echo ""

# 等待後端啟動
sleep 3

# 啟動前端
cd ../frontend
echo "🚀 啟動前端服務..."
echo "──────────────────────────────────────────────────────────────"
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo "✅ 前端服務已啟動 (PID: $FRONTEND_PID)"
echo "   URL: http://localhost:3000/index_gemini.html"
echo ""

# 顯示使用說明
echo "═══════════════════════════════════════════════════════════════"
echo "✨ 服務已啟動！"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📖 使用方式："
echo "   1. 開啟瀏覽器: http://localhost:3000/index_gemini.html"
echo "   2. 與 AI 對話描述您的創作需求"
echo "   3. 上傳參考圖（可選）"
echo "   4. 等待 Prompt 準備完成"
echo "   5. 點擊「開始生成」"
echo ""
echo "🛑 停止服務："
echo "   按 Ctrl+C 或執行: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 等待用戶中斷
trap "echo ''; echo '🛑 正在停止服務...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ 服務已停止'; exit 0" INT

# 保持腳本運行
wait
