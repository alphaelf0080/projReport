#!/bin/bash
# macOS 專用安裝腳本

echo "🎨 Slot Game Concept Art Generator - macOS 安裝"
echo "================================================"

# 檢查 Python 版本
echo "📌 檢查 Python 版本..."
python3 --version

# 安裝基礎依賴
echo ""
echo "📦 安裝基礎依賴..."
pip3 install -r requirements-macos.txt

# 安裝 PyTorch (macOS 專用)
echo ""
echo "🔥 安裝 PyTorch (macOS 版本)..."
echo "⚠️  注意：macOS 使用 CPU 版本，或使用 MPS (Metal Performance Shaders) 加速"

# 檢查是否為 Apple Silicon (M1/M2/M3)
if [[ $(uname -m) == 'arm64' ]]; then
    echo "✅ 偵測到 Apple Silicon (ARM64)"
    echo "   安裝支援 MPS 的 PyTorch..."
    pip3 install torch torchvision torchaudio
else
    echo "✅ 偵測到 Intel Mac (x86_64)"
    echo "   安裝 CPU 版本 PyTorch..."
    pip3 install torch torchvision torchaudio
fi

echo ""
echo "✅ 安裝完成！"
echo ""
echo "📋 下一步："
echo "   1. 測試安裝：python3 test_installation.py"
echo "   2. 啟動服務：python3 main.py"
echo "   3. 訪問 API 文檔：http://localhost:8000/docs"
echo ""
echo "⚠️  首次生成圖像時會下載 SDXL 模型（約 6-7GB）"
echo "⚠️  macOS 上建議使用 Apple Silicon (M1/M2/M3) 以獲得 MPS 加速"
echo ""
