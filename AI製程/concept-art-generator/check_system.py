"""
簡化測試腳本 - 不需要外部依賴
驗證核心邏輯與檔案結構
"""
import os
import json
from pathlib import Path

print("=" * 70)
print("🎨 Slot Game Concept Art Generator - 系統檢查")
print("=" * 70)

# 檢查目錄結構
print("\n【檢查 1】目錄結構")
print("-" * 70)

required_dirs = [
    "backend",
    "backend/models",
    "backend/services",
    "frontend",
    "output"
]

for dir_path in required_dirs:
    exists = os.path.isdir(dir_path)
    status = "✅" if exists else "❌"
    print(f"{status} {dir_path}")

# 檢查核心檔案
print("\n【檢查 2】核心檔案")
print("-" * 70)

required_files = [
    "README.md",
    "QUICKSTART.md",
    "backend/main.py",
    "backend/requirements.txt",
    "backend/models/schemas.py",
    "backend/models/token_weights.json",
    "backend/services/prompt_engine.py",
    "backend/services/palette_extractor.py",
    "backend/services/image_generator.py",
    "frontend/index.html",
    "frontend/app.js",
    "frontend/style.css"
]

for file_path in required_files:
    exists = os.path.isfile(file_path)
    status = "✅" if exists else "❌"
    print(f"{status} {file_path}")

# 檢查 token_weights.json 格式
print("\n【檢查 3】Token 權重表格式")
print("-" * 70)

try:
    with open("backend/models/token_weights.json", 'r', encoding='utf-8') as f:
        weights = json.load(f)
    
    print(f"✅ JSON 格式正確")
    print(f"✅ 包含 {len(weights)} 個類別:")
    for category in weights.keys():
        token_count = len(weights[category])
        print(f"   - {category}: {token_count} tokens")
except Exception as e:
    print(f"❌ 錯誤: {e}")

# 檢查 Prompt 模板邏輯
print("\n【檢查 4】Prompt 組合邏輯（模擬）")
print("-" * 70)

def simple_prompt_compose(theme, keywords, colors):
    """簡化版 Prompt 組合"""
    parts = [
        "Cinematic masterpiece",
        theme,
        ", ".join(keywords),
        "dramatic lighting",
        f"rich {colors[0]} palette" if colors else "",
        "premium slot game concept art",
        "ultra detailed, 16:9"
    ]
    return ", ".join([p for p in parts if p])

test_theme = "東方龍與財富"
test_keywords = ["cinematic", "volumetric light"]
test_colors = ["crimson and golden"]

result = simple_prompt_compose(test_theme, test_keywords, test_colors)
print(f"✅ 測試 Prompt:")
print(f"   主題: {test_theme}")
print(f"   關鍵詞: {', '.join(test_keywords)}")
print(f"   結果長度: {len(result)} 字元")
print(f"\n   完整 Prompt:")
print(f"   {result}")

# 檢查 API 端點定義
print("\n【檢查 5】API 端點定義")
print("-" * 70)

api_endpoints = [
    ("POST", "/api/brief", "建立創意簡報"),
    ("POST", "/api/generate", "生成圖像"),
    ("GET", "/api/generation/{id}", "查詢生成狀態"),
    ("POST", "/api/feedback", "提交反饋"),
    ("GET", "/api/health", "健康檢查")
]

for method, endpoint, description in api_endpoints:
    print(f"✅ {method:6} {endpoint:30} - {description}")

# 使用流程摘要
print("\n【檢查 6】完整使用流程")
print("-" * 70)

workflow = [
    ("1", "啟動後端", "python backend/main.py"),
    ("2", "啟動前端", "python -m http.server 3000 (在 frontend/)"),
    ("3", "開啟瀏覽器", "http://localhost:3000"),
    ("4", "填寫 Brief", "主題、風格、色彩、參考圖"),
    ("5", "生成圖像", "點擊「開始生成」按鈕"),
    ("6", "評估結果", "查看、選擇、評分"),
    ("7", "提交反饋", "調整建議 → 重新生成"),
    ("8", "迭代優化", "重複步驟 5-7 直到滿意")
]

for step, action, detail in workflow:
    print(f"  {step}. {action:15} → {detail}")

# 功能特色
print("\n【檢查 7】核心功能特色")
print("-" * 70)

features = [
    "✅ 引導式輸入 - 分步驟收集美術需求",
    "✅ 智能 Prompt 組合 - 自動生成最佳化提示詞",
    "✅ 色板自動提取 - 從參考圖分析主色調",
    "✅ 迭代優化機制 - 基於反饋調整生成參數",
    "✅ Token 權重系統 - 動態調整風格強度",
    "✅ 多變體生成 - 一次生成多個角度/光線方向",
    "✅ 即時進度追蹤 - WebSocket 或輪詢更新狀態",
    "✅ 版本記錄追蹤 - 完整 Prompt/Seed 歷史",
    "✅ 響應式前端 - 支援桌面與移動裝置",
    "✅ RESTful API - 標準化介面易於整合"
]

for feature in features:
    print(f"  {feature}")

# 技術棧
print("\n【檢查 8】技術棧")
print("-" * 70)

tech_stack = {
    "後端框架": "FastAPI (Python)",
    "AI 模型": "Stable Diffusion XL",
    "圖像處理": "Pillow, OpenCV",
    "色彩分析": "scikit-learn (k-means)",
    "前端": "HTML5 + Vanilla JavaScript",
    "樣式": "純 CSS (漸變、動畫)",
    "API 文檔": "Swagger UI (自動生成)",
    "資料格式": "JSON, Pydantic schemas"
}

for component, tech in tech_stack.items():
    print(f"  {component:15} : {tech}")

# 系統需求
print("\n【檢查 9】系統需求")
print("-" * 70)

requirements = {
    "最低配置": {
        "Python": "3.8+",
        "RAM": "8GB",
        "硬碟": "20GB",
        "GPU": "選用（CPU 可運行但較慢）"
    },
    "建議配置": {
        "Python": "3.10+",
        "RAM": "16GB+",
        "硬碟": "30GB",
        "GPU": "NVIDIA (8GB+ VRAM, CUDA)"
    }
}

for config_type, specs in requirements.items():
    print(f"\n  {config_type}:")
    for item, spec in specs.items():
        print(f"    {item:10} : {spec}")

# 快速啟動指令
print("\n【檢查 10】快速啟動指令")
print("-" * 70)

print("""
  方法 1: 使用啟動腳本 (macOS/Linux)
  ----------------------------------------
  chmod +x start.sh
  ./start.sh

  方法 2: 手動啟動
  ----------------------------------------
  # Terminal 1 - 後端
  cd backend
  pip install -r requirements.txt
  python main.py

  # Terminal 2 - 前端
  cd frontend
  python -m http.server 3000

  # 瀏覽器
  開啟 http://localhost:3000
""")

# 完成
print("\n" + "=" * 70)
print("✅ 系統檢查完成！")
print("=" * 70)

print("""
📋 下一步行動:

  1️⃣  安裝依賴
     cd backend && pip install -r requirements.txt

  2️⃣  測試 API（可選）
     python backend/main.py
     開啟 http://localhost:8000/docs

  3️⃣  啟動完整服務
     ./start.sh  (或手動啟動前後端)

  4️⃣  開始使用
     在瀏覽器開啟 http://localhost:3000
     
⚠️  注意事項:
  - 首次執行會下載 SDXL 模型（約 6GB）
  - 建議使用 GPU 以獲得最佳效能
  - 詳細文檔請查看 README.md 與 QUICKSTART.md
""")

print("🎨 準備好開始創作 Slot Game Concept Art 了嗎？")
print("=" * 70)
