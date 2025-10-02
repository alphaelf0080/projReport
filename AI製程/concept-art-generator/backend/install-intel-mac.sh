#!/bin/bash
# macOS Intel 專用安裝腳本 - 使用官方 PyTorch 源

echo "🎨 Slot Game Concept Art Generator - macOS Intel 安裝"
echo "================================================"
echo ""
echo "⚠️  偵測到 Intel Mac"
echo "⚠️  PyTorch 官方 pip 源可能不支援 macOS Intel"
echo ""
echo "建議使用以下方案之一："
echo ""
echo "方案 1️⃣ : 使用 Conda (推薦)"
echo "--------------------------------------"
echo "# 安裝 Conda"
echo "brew install --cask miniconda"
echo ""
echo "# 創建環境並安裝"
echo "conda create -n concept-art python=3.10"
echo "conda activate concept-art"
echo "conda install pytorch torchvision -c pytorch"
echo "pip install -r requirements-macos.txt"
echo ""
echo ""
echo "方案 2️⃣ : 使用舊版 PyTorch (pip)"
echo "--------------------------------------"
echo "pip3 install torch==1.13.1 torchvision==0.14.1"
echo "pip3 install -r requirements-macos.txt"
echo ""
echo ""
echo "方案 3️⃣ : 使用 CPU-only 模擬 (測試用)"
echo "--------------------------------------"
echo "# 安裝不含 torch 的依賴"
echo "pip3 install fastapi uvicorn[standard] pydantic python-multipart"
echo "pip3 install Pillow opencv-python scikit-learn colormath loguru"
echo ""
echo "# 創建 torch 模擬模組（僅供測試 API，無法實際生成圖像）"
echo "mkdir -p mock_torch"
echo "cat > mock_torch/__init__.py << 'EOF'"
echo '"""Mock torch for testing without GPU"""'
echo 'class MockModule:'
echo '    def __init__(self, name): self.name = name'
echo '    def __getattr__(self, item): return MockModule(f"{self.name}.{item}")'
echo '    def __call__(self, *args, **kwargs): return MockModule(self.name)'
echo ''
echo '__version__ = "2.0.0"'
echo 'cuda = MockModule("cuda")'
echo 'backends = MockModule("backends")'
echo 'EOF'
echo ""
echo ""
echo "您想使用哪個方案？"
echo "建議：如果您有 Conda，使用方案 1"
echo "      如果只想測試 API，使用方案 3"
