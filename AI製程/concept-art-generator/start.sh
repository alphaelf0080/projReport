#!/bin/bash
# 快速啟動腳本 - macOS/Linux

echo "🎨 Slot Game Concept Art Generator - 啟動中..."
echo ""

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 未安裝 Python 3"
    echo "請先安裝 Python 3.8+"
    exit 1
fi

# 建立虛擬環境（如果不存在）
if [ ! -d "backend/venv" ]; then
    echo "📦 建立 Python 虛擬環境..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source backend/venv/bin/activate

# 安裝依賴（如果需要）
if [ ! -f "backend/.deps_installed" ]; then
    echo "📥 安裝 Python 依賴..."
    pip install -r backend/requirements.txt
    touch backend/.deps_installed
fi

# 啟動後端
echo ""
echo "🚀 啟動後端服務..."
echo "   後端 API: http://localhost:8000"
echo "   API 文檔: http://localhost:8000/docs"
echo ""
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# 等待後端啟動
sleep 3

# 啟動前端
echo "🌐 啟動前端服務..."
echo "   前端網址: http://localhost:3000"
echo ""
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 服務啟動完成！"
echo ""
echo "📖 使用說明:"
echo "   1. 在瀏覽器開啟 http://localhost:3000"
echo "   2. 填寫創意簡報（主題、風格、色彩）"
echo "   3. 點擊「生成」等待 AI 產生圖像"
echo "   4. 評估結果並提供反饋"
echo ""
echo "⚠️  注意:"
echo "   - 首次執行會下載約 6GB 模型，請確保網路暢通"
echo "   - 需要 GPU (CUDA) 以獲得最佳效能"
echo "   - 按 Ctrl+C 停止服務"
echo ""

# 等待使用者中斷
wait

# 清理
echo ""
echo "🛑 正在停止服務..."
kill $BACKEND_PID 2>/dev/null
kill $FRONTEND_PID 2>/dev/null
echo "✅ 已停止"
