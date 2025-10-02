"""
Gemini Agent - 使用 Google Gemini 作為對話式 AI 代理
負責與美術人員互動，收集需求，生成 Prompt
"""
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from loguru import logger
import json
import os
from pathlib import Path

class GeminiConceptAgent:
    """
    對話式 Concept Art 生成代理
    使用 Gemini 理解美術需求並生成最佳化 Prompt
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化 Gemini Agent"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("需要 GEMINI_API_KEY 環境變數")
        
        genai.configure(api_key=self.api_key)
        
        # 使用最新的 Gemini 2.5 Flash（快速、便宜）
        # 其他選項: 'gemini-2.5-pro', 'gemini-2.0-flash', 'gemini-flash-latest'
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 對話歷史
        self.chat_history = []
        
        # 系統提示詞 - 專業 Slot Game 美術顧問
        self.system_prompt = self._load_system_prompt()
        
        logger.info("Gemini Concept Agent 初始化完成")
    
    def _load_system_prompt(self) -> str:
        """載入系統提示詞"""
        return """你是一位專業的 Slot Game Concept Art 創意總監，具備以下專長：

【角色定位】
- 資深遊戲美術總監，專精 Slot Game 視覺設計
- 精通東方、西方、奇幻、科技等多種主題風格
- 深度了解 Stable Diffusion、DALL-E 等 AI 繪圖工具的 Prompt 工程
- 擅長色彩理論、構圖法則、光影氛圍營造

【核心任務】
1. **需求收集** - 引導美術人員提供：
   - 遊戲主題（Theme）：如東方龍、維京戰士、埃及神話
   - 視覺風格（Style）：寫實、卡通、賽博朋克、水墨
   - 色彩偏好（Color）：主色調、輔助色、氛圍色
   - 參考素材（Reference）：類似作品、靈感來源

2. **Prompt 生成** - 根據需求產出結構化提示詞：
   - 遵循 8 層結構：前言 + 主體 + 構圖 + 光線 + 材質 + 氛圍 + 色彩 + 技術參數
   - 使用專業術語：cinematic lighting, volumetric fog, golden ratio
   - 針對 Slot Game 特性：高對比、豐富細節、吸睛主角

3. **互動優化** - 迭代式改進：
   - 分析美術人員對生成結果的反饋
   - 調整 Token 權重和關鍵詞
   - 提供 3-5 個變體方案

【對話風格】
- 專業但友善，使用繁體中文
- 主動詢問關鍵細節（如角度、光源方向、情緒氛圍）
- 每次提供具體建議和範例
- 簡潔回應，避免冗長說明

【輸出格式】
當美術人員提供完整需求後，以 JSON 格式輸出：
```json
{
  "theme": "主題描述",
  "style_tags": ["風格標籤1", "風格標籤2"],
  "composition": "構圖建議",
  "lighting": "光線設定",
  "color_palette": ["主色", "輔助色", "強調色"],
  "mood": "情緒氛圍",
  "prompt": "完整的 AI 生成提示詞",
  "negative_prompt": "負面提示詞",
  "suggestions": ["建議1", "建議2"]
}
```

現在開始擔任 Slot Game 美術顧問，引導美術人員創作出色的 Concept Art！
"""
    
    async def chat(self, user_message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        與使用者對話
        
        Args:
            user_message: 使用者訊息
            context: 額外上下文（色板、參考圖分析等）
        
        Returns:
            {
                "response": "AI 回應",
                "prompt_ready": False,  # 是否準備好生成
                "prompt_data": {...}  # 如果 ready，包含完整 Prompt 資料
            }
        """
        try:
            # 構建完整訊息（包含上下文）
            full_message = user_message
            if context:
                full_message = f"{user_message}\n\n【上下文資訊】\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            
            # 如果是第一次對話，加入系統提示詞
            if not self.chat_history:
                # 創建新對話，包含系統提示
                chat = self.model.start_chat(history=[])
                # 先發送系統提示
                response = chat.send_message(self.system_prompt)
                logger.info("系統提示詞已發送")
            else:
                # 從歷史記錄恢復對話
                chat = self.model.start_chat(history=self.chat_history)
            
            # 發送使用者訊息
            response = chat.send_message(full_message)
            response_text = response.text
            
            # 更新對話歷史
            self.chat_history.append({
                "role": "user",
                "parts": [full_message]
            })
            self.chat_history.append({
                "role": "model",
                "parts": [response_text]
            })
            
            # 檢查是否包含 JSON 格式的 Prompt（表示可以開始生成）
            prompt_data = self._extract_json_from_response(response_text)
            
            result = {
                "response": response_text,
                "prompt_ready": prompt_data is not None,
                "prompt_data": prompt_data
            }
            
            logger.info(f"Gemini 回應長度: {len(response_text)}, Prompt Ready: {result['prompt_ready']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Gemini 對話錯誤: {e}")
            return {
                "response": f"抱歉，發生錯誤: {str(e)}",
                "prompt_ready": False,
                "prompt_data": None
            }
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict]:
        """從回應中提取 JSON 格式的 Prompt 資料"""
        try:
            # 查找 JSON 代碼塊
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
            elif "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
            else:
                return None
            
            # 解析 JSON
            data = json.loads(json_str)
            
            # 驗證必要欄位
            required_fields = ["theme", "prompt"]
            if all(field in data for field in required_fields):
                return data
            
            return None
            
        except Exception as e:
            logger.debug(f"JSON 提取失敗: {e}")
            return None
    
    def analyze_reference_image(self, image_analysis: Dict) -> str:
        """
        分析參考圖並生成描述
        
        Args:
            image_analysis: 圖像分析結果（色板、物件等）
        
        Returns:
            自然語言描述
        """
        colors = image_analysis.get("color_palette", [])
        color_desc = ", ".join(colors[:3]) if colors else "未提供"
        
        description = f"""
參考圖分析結果：
- 主要色調：{color_desc}
- 色彩數量：{len(colors)} 種
- 建議：可使用這些色彩作為主色調
"""
        return description
    
    def reset_conversation(self):
        """重置對話歷史"""
        self.chat_history = []
        logger.info("對話歷史已重置")
    
    def get_conversation_summary(self) -> str:
        """獲取對話摘要"""
        if not self.chat_history:
            return "尚未開始對話"
        
        user_messages = [msg for msg in self.chat_history if msg["role"] == "user"]
        return f"共 {len(user_messages)} 輪對話"


class GeminiImageGenerator:
    """
    使用 Gemini + Imagen 生成圖像
    注意：Imagen 需要單獨申請 API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化圖像生成器"""
        self.api_key = api_key or os.getenv("IMAGEN_API_KEY")
        logger.info("Gemini Image Generator 初始化")
    
    async def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_images: int = 4,
        aspect_ratio: str = "16:9",
        **kwargs
    ) -> List[str]:
        """
        生成圖像（使用 Imagen API 或其他服務）
        
        Returns:
            圖像 URL 列表
        """
        # TODO: 實作 Imagen API 呼叫
        # 目前返回佔位符
        logger.warning("Imagen API 尚未實作，返回佔位符")
        
        placeholder_urls = [
            f"https://via.placeholder.com/1024x576?text=Concept+{i+1}"
            for i in range(num_images)
        ]
        
        return placeholder_urls


# 使用範例
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        # 需要設定環境變數 GEMINI_API_KEY
        agent = GeminiConceptAgent()
        
        # 模擬對話
        print("=" * 70)
        print("測試 Gemini Concept Agent")
        print("=" * 70)
        
        # 第一輪：美術人員說明需求
        result1 = await agent.chat(
            "我想做一個東方龍主題的 Slot Game，風格要華麗、金碧輝煌"
        )
        print(f"\n【AI】: {result1['response']}")
        print(f"Prompt Ready: {result1['prompt_ready']}")
        
        # 第二輪：補充細節
        result2 = await agent.chat(
            "我希望主角是一條紅色的龍，背景有金色的雲彩，整體要有電影感的打光"
        )
        print(f"\n【AI】: {result2['response']}")
        print(f"Prompt Ready: {result2['prompt_ready']}")
        
        if result2['prompt_ready']:
            print(f"\n【生成的 Prompt】:")
            print(json.dumps(result2['prompt_data'], ensure_ascii=False, indent=2))
    
    # asyncio.run(test_agent())
    print("提示：需要設定 GEMINI_API_KEY 環境變數才能執行測試")
