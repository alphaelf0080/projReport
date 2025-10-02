"""
測試 Prompt Engine 與 Palette Extractor
"""
import sys
sys.path.append('backend')

from services.prompt_engine import PromptEngine
from services.palette_extractor import PaletteExtractor
from PIL import Image
import numpy as np

print("=" * 60)
print("🧪 測試 Slot Game Concept Art Generator")
print("=" * 60)

# ========== 測試 1: Prompt Engine ==========
print("\n【測試 1】Prompt Engine - 組合 Prompt")
print("-" * 60)

engine = PromptEngine()

# 測試案例：東方龍主題
prompt, neg = engine.compose_prompt(
    theme="東方龍與財富",
    style_keywords=["cinematic", "volumetric light", "ornate"],
    color_hex=["#B30012", "#CFA64D"],
    ratio="16:9"
)

print("✅ Positive Prompt:")
print(prompt)
print("\n✅ Negative Prompt:")
print(neg)

# 測試變體生成
print("\n【測試 2】生成 Prompt 變體")
print("-" * 60)

variations = engine.generate_variations(prompt, count=3)
for i, var in enumerate(variations, 1):
    print(f"\n變體 {i}:")
    print(var[:150] + "..." if len(var) > 150 else var)

# ========== 測試 3: Palette Extractor ==========
print("\n【測試 3】Palette Extractor - 色板提取")
print("-" * 60)

extractor = PaletteExtractor(n_colors=6)

# 建立測試圖片（模擬參考圖）
print("建立測試圖片...")
width, height = 200, 200
test_img = Image.new('RGB', (width, height))
pixels = test_img.load()

test_colors = [
    (179, 0, 18),    # 深紅
    (207, 166, 77),  # 金色
    (255, 215, 0),   # 金黃
    (50, 50, 50),    # 深灰
    (255, 100, 100), # 淺紅
    (180, 140, 70)   # 棕金
]

for y in range(height):
    for x in range(width):
        color_idx = (x // 40 + y // 40) % len(test_colors)
        pixels[x, y] = test_colors[color_idx]

# 提取色板
hex_colors = extractor.extract_from_image(test_img)

print(f"✅ 提取到 {len(hex_colors)} 個主色:")
for i, hex_code in enumerate(hex_colors, 1):
    print(f"   {i}. {hex_code}")

# 分類色彩
categorized = extractor.categorize_colors(hex_colors)
print("\n✅ 色彩分類:")
print(f"   主色: {categorized['primary']}")
print(f"   輔色: {categorized['secondary']}")
print(f"   點綴色: {categorized['accent']}")

# 生成描述
description = extractor.generate_palette_description(hex_colors)
print(f"\n✅ 色彩描述: {description}")

# ========== 測試 4: 權重更新 ==========
print("\n【測試 4】Token 權重更新")
print("-" * 60)

# 模擬反饋
feedback = {
    "selections": ["img_a", "img_b"],
    "ratings": {"img_a": 5, "img_b": 4},
    "tags": {
        "img_c": ["lighting too flat"]
    }
}

updated = engine.update_weights(feedback)

print(f"✅ 更新了 {len(updated)} 個權重:")
for token, weight in list(updated.items())[:5]:
    print(f"   {token}: {weight:.2f}")

# ========== 測試 5: 完整流程模擬 ==========
print("\n【測試 5】完整流程模擬")
print("-" * 60)

print("步驟 1: 收集 Brief")
brief = {
    "theme": "埃及法老與金字塔",
    "styleKeywords": ["dramatic lighting", "ornate", "mystical"],
    "colors": ["#C4A544", "#4169E1"]
}
print(f"   主題: {brief['theme']}")
print(f"   風格: {', '.join(brief['styleKeywords'])}")

print("\n步驟 2: 生成 Prompt")
final_prompt, final_neg = engine.compose_prompt(
    theme=brief["theme"],
    style_keywords=brief["styleKeywords"],
    color_hex=brief["colors"],
    ratio="16:9"
)
print(f"   ✅ Prompt 長度: {len(final_prompt)} 字元")

print("\n步驟 3: （模擬）發送至圖像生成器")
print("   [此處會調用 SDXL 生成圖像]")

print("\n步驟 4: （模擬）收集反饋並調整")
print("   使用者選擇圖像 → 更新權重 → 重新生成")

print("\n" + "=" * 60)
print("✅ 所有測試完成！")
print("=" * 60)

print("\n📝 下一步:")
print("   1. 安裝依賴: pip install -r backend/requirements.txt")
print("   2. 啟動後端: python backend/main.py")
print("   3. 啟動前端: python -m http.server 3000 (在 frontend/ 目錄)")
print("   4. 開啟瀏覽器: http://localhost:3000")
print("\n⚠️  注意: 首次執行會下載約 6GB 模型，請確保網路暢通")
