#!/usr/bin/env python3
"""
測試 Gemini API 連線
"""
import sys
import os

# 添加 backend 目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.gemini_agent import GeminiConceptAgent
import asyncio

async def test_gemini():
    print("=" * 70)
    print("🧪 測試 Gemini Concept Agent")
    print("=" * 70)
    print()
    
    try:
        # 初始化 Agent
        print("1️⃣  初始化 Gemini Agent...")
        agent = GeminiConceptAgent()
        print("   ✅ 初始化成功")
        print()
        
        # 測試對話
        print("2️⃣  測試對話功能...")
        test_message = "我想做一個東方龍主題的 Slot Game，風格要華麗金碧輝煌"
        print(f"   使用者: {test_message}")
        print()
        
        result = await agent.chat(test_message)
        
        print("   🤖 AI 回應:")
        print("   " + "-" * 66)
        # 顯示前 500 字元
        response_preview = result['response'][:500]
        print(f"   {response_preview}")
        if len(result['response']) > 500:
            print(f"   ... (共 {len(result['response'])} 字元)")
        print("   " + "-" * 66)
        print()
        
        # 檢查狀態
        print("3️⃣  檢查回應狀態...")
        print(f"   - Prompt Ready: {result['prompt_ready']}")
        print(f"   - 回應長度: {len(result['response'])} 字元")
        print()
        
        if result['prompt_ready']:
            print("   ✅ Prompt 已準備就緒！")
            print(f"   - 主題: {result['prompt_data'].get('theme', 'N/A')}")
            print(f"   - 風格: {result['prompt_data'].get('style_tags', [])}")
        else:
            print("   ℹ️  Prompt 尚未準備（需要更多對話）")
        
        print()
        print("=" * 70)
        print("✅ 測試完成！Gemini Agent 運作正常")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ 測試失敗: {e}")
        print("=" * 70)
        print()
        print("💡 可能的原因:")
        print("   1. GEMINI_API_KEY 未設定或無效")
        print("   2. 網路連線問題")
        print("   3. API 配額已用盡")
        print()
        print("🔧 解決方案:")
        print("   1. 檢查 .env 檔案中的 GEMINI_API_KEY")
        print("   2. 確認 API Key 有效: https://makersuite.google.com/app/apikey")
        print("   3. 檢查網路連線")
        print()
        return False

if __name__ == "__main__":
    print()
    success = asyncio.run(test_gemini())
    print()
    
    if success:
        print("🎉 您可以開始使用系統了！")
        print()
        print("📋 下一步:")
        print("   1. 啟動前端: cd ../frontend && python3 -m http.server 3000")
        print("   2. 開啟瀏覽器: http://localhost:3000/index_gemini.html")
        print()
    else:
        print("⚠️  請修正上述問題後再試")
        print()
        sys.exit(1)
