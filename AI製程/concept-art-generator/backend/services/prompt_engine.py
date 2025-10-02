"""
Prompt 組合引擎
負責根據輸入參數與 Token 權重組合最佳化的 Prompt
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from loguru import logger


class PromptEngine:
    """Prompt 組合與優化引擎"""
    
    def __init__(self, weights_path: str = "backend/models/token_weights.json"):
        """初始化引擎，載入 Token 權重表"""
        self.weights_path = Path(weights_path)
        self.weights = self._load_weights()
        
        # Prompt 結構模板
        self.template_structure = [
            "preamble",      # 前言（風格定調）
            "subject",       # 主體描述
            "composition",   # 構圖
            "lighting",      # 光線
            "material",      # 材質/細節
            "atmosphere",    # 氣氛
            "color",         # 色彩
            "technical"      # 技術參數
        ]
        
    def _load_weights(self) -> Dict:
        """載入 Token 權重表"""
        if not self.weights_path.exists():
            logger.warning(f"權重表不存在: {self.weights_path}，使用預設值")
            return self._default_weights()
        
        with open(self.weights_path, 'r', encoding='utf-8') as f:
            weights = json.load(f)
        logger.info(f"已載入 {len(weights)} 個權重類別")
        return weights
    
    def _default_weights(self) -> Dict:
        """預設權重表"""
        return {
            "lighting": {"volumetric light": 1.0, "dramatic rim light": 1.0},
            "material": {"ornate": 1.0, "intricate": 1.0},
            "composition": {"cinematic composition": 1.0},
            "atmosphere": {"majestic": 1.0},
            "detail": {"ultra detailed": 1.0}
        }
    
    def compose_prompt(
        self,
        theme: str,
        style_keywords: List[str],
        color_hex: List[str],
        ratio: str = "16:9",
        variation: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        組合完整 Prompt
        
        Args:
            theme: 主題（例：「東方龍與財富」）
            style_keywords: 風格關鍵詞列表
            color_hex: 色彩 HEX 列表
            ratio: 圖像比例
            variation: 變體要求（例：close-up, wide angle）
        
        Returns:
            (positive_prompt, negative_prompt)
        """
        # 1. 前言層：風格定調
        preamble = self._build_preamble(style_keywords)
        
        # 2. 主體層：主題轉換
        subject = self._build_subject(theme, variation)
        
        # 3. 構圖層
        composition = self._build_composition(style_keywords, variation)
        
        # 4. 光線層
        lighting = self._build_lighting(style_keywords)
        
        # 5. 材質/細節層
        material = self._build_material(style_keywords)
        
        # 6. 氣氛層
        atmosphere = self._build_atmosphere(theme)
        
        # 7. 色彩層
        color = self._build_color(color_hex)
        
        # 8. 技術參數層
        technical = self._build_technical(ratio)
        
        # 組合所有層
        positive_parts = [
            preamble, subject, composition, lighting,
            material, atmosphere, color, technical
        ]
        positive_prompt = ", ".join([p for p in positive_parts if p])
        
        # 組合負面 Prompt
        negative_prompt = self._build_negative()
        
        logger.info(f"已生成 Prompt (長度: {len(positive_prompt)})")
        return positive_prompt, negative_prompt
    
    def _build_preamble(self, keywords: List[str]) -> str:
        """建立前言層"""
        # 根據關鍵詞決定風格強度
        if "cinematic" in keywords:
            return "Cinematic masterpiece"
        elif "artistic" in keywords:
            return "Artistic concept art"
        elif "realistic" in keywords:
            return "Photorealistic rendering"
        return "Premium quality artwork"
    
    def _build_subject(self, theme: str, variation: Optional[str]) -> str:
        """建立主體層"""
        # 主題語意轉換（簡化版，實際可用 LLM）
        theme_map = {
            "東方龍": "majestic oriental dragon",
            "財富": "surrounded by treasures and golden coins",
            "埃及": "ancient Egyptian pharaoh",
            "海盜": "rugged pirate captain",
            "魔幻": "mystical wizard"
        }
        
        subject_parts = []
        for key, desc in theme_map.items():
            if key in theme:
                subject_parts.append(desc)
        
        if not subject_parts:
            subject_parts.append(theme)  # 直接使用原文
        
        # 加入變體描述
        if variation:
            variation_map = {
                "close-up": "close-up portrait",
                "wide angle": "wide angle view",
                "aerial": "aerial perspective",
                "top view": "top-down view"
            }
            if variation in variation_map:
                subject_parts.insert(0, variation_map[variation])
        
        return " ".join(subject_parts)
    
    def _build_composition(self, keywords: List[str], variation: Optional[str]) -> str:
        """建立構圖層"""
        comps = []
        
        # 從權重表選擇構圖 token
        comp_tokens = self.weights.get("composition", {})
        for token, weight in sorted(comp_tokens.items(), key=lambda x: x[1], reverse=True)[:2]:
            if weight >= 0.9:
                comps.append(self._apply_weight(token, weight))
        
        # 變體特定構圖
        if variation:
            if "close" in variation:
                comps.append("shallow depth of field")
            elif "wide" in variation:
                comps.append("expansive landscape")
        
        return ", ".join(comps) if comps else "dynamic composition"
    
    def _build_lighting(self, keywords: List[str]) -> str:
        """建立光線層"""
        lights = []
        
        # 從關鍵詞與權重表組合
        light_tokens = self.weights.get("lighting", {})
        
        # 優先選擇高權重 token
        for token, weight in sorted(light_tokens.items(), key=lambda x: x[1], reverse=True)[:3]:
            if any(kw in token for kw in keywords) or weight >= 1.0:
                lights.append(self._apply_weight(token, weight))
        
        return ", ".join(lights) if lights else "dramatic lighting"
    
    def _build_material(self, keywords: List[str]) -> str:
        """建立材質/細節層"""
        materials = []
        
        mat_tokens = self.weights.get("material", {})
        detail_tokens = self.weights.get("detail", {})
        
        # 選擇材質 token
        for token, weight in sorted(mat_tokens.items(), key=lambda x: x[1], reverse=True)[:2]:
            if weight >= 0.9:
                materials.append(self._apply_weight(token, weight))
        
        # 選擇細節 token
        for token, weight in sorted(detail_tokens.items(), key=lambda x: x[1], reverse=True)[:2]:
            if weight >= 0.9:
                materials.append(self._apply_weight(token, weight))
        
        return ", ".join(materials) if materials else "intricate details"
    
    def _build_atmosphere(self, theme: str) -> str:
        """建立氣氛層"""
        atmos = []
        
        atmo_tokens = self.weights.get("atmosphere", {})
        
        # 根據主題選擇氣氛
        theme_atmo_map = {
            "龍": ["majestic", "epic"],
            "財富": ["luxurious", "opulent"],
            "神秘": ["mysterious", "ethereal"],
            "戰鬥": ["energetic", "dramatic"]
        }
        
        for key, atmo_list in theme_atmo_map.items():
            if key in theme:
                for a in atmo_list:
                    if a in atmo_tokens:
                        atmos.append(self._apply_weight(a, atmo_tokens[a]))
        
        if not atmos:
            # 預設選擇最高權重
            top_atmo = sorted(atmo_tokens.items(), key=lambda x: x[1], reverse=True)[:1]
            atmos = [self._apply_weight(t, w) for t, w in top_atmo]
        
        return ", ".join(atmos) if atmos else "epic atmosphere"
    
    def _build_color(self, color_hex: List[str]) -> str:
        """建立色彩層"""
        if not color_hex:
            return ""
        
        # HEX 轉色彩描述（簡化版）
        color_names = []
        for hex_code in color_hex[:3]:  # 最多 3 個主色
            color_name = self._hex_to_color_name(hex_code)
            if color_name:
                color_names.append(color_name)
        
        if color_names:
            return f"rich {' and '.join(color_names)} palette"
        return ""
    
    def _hex_to_color_name(self, hex_code: str) -> str:
        """HEX 轉色彩名稱（簡化映射）"""
        hex_code = hex_code.lstrip('#').upper()
        
        # 簡化色彩映射
        color_map = {
            'B30012': 'crimson',
            'D41F27': 'ruby red',
            'CFA64D': 'golden',
            'F7E09A': 'pale gold',
            'FFD700': 'gold',
            '4169E1': 'royal blue',
            '32CD32': 'emerald green'
        }
        
        # 精確匹配
        if hex_code in color_map:
            return color_map[hex_code]
        
        # 簡單範圍判斷（R, G, B 主導）
        try:
            r = int(hex_code[0:2], 16)
            g = int(hex_code[2:4], 16)
            b = int(hex_code[4:6], 16)
            
            if r > g and r > b:
                return "red" if r > 180 else "crimson"
            elif g > r and g > b:
                return "emerald" if g > 180 else "forest green"
            elif b > r and b > g:
                return "sapphire" if b > 180 else "deep blue"
            elif r > 200 and g > 180:
                return "golden"
            else:
                return "neutral"
        except:
            return ""
    
    def _build_technical(self, ratio: str) -> str:
        """建立技術參數層"""
        tech_parts = [
            "premium slot game concept art",
            "ultra detailed",
            "high fidelity",
            ratio
        ]
        return ", ".join(tech_parts)
    
    def _build_negative(self) -> str:
        """建立負面 Prompt"""
        neg_tokens = self.weights.get("negative_tokens", {})
        
        # 選擇高權重負面詞
        negatives = []
        for token, weight in sorted(neg_tokens.items(), key=lambda x: x[1], reverse=True):
            if weight >= 1.2:
                negatives.append(token)
        
        if not negatives:
            negatives = [
                "low quality", "blurry", "watermark", "distorted",
                "extra limbs", "flat lighting", "noisy background"
            ]
        
        return ", ".join(negatives)
    
    def _apply_weight(self, token: str, weight: float) -> str:
        """
        應用 Token 權重（生成帶權重語法）
        例：weight=1.2 → (token:1.2)
        """
        if weight == 1.0:
            return token
        elif weight > 1.0:
            return f"({token}:{weight:.2f})"
        else:
            return f"[{token}:{weight:.2f}]"  # 降權語法
    
    def update_weights(self, feedback: Dict[str, any]) -> Dict[str, float]:
        """
        根據反饋更新權重
        
        Args:
            feedback: 包含 selections, ratings, tags
        
        Returns:
            更新後的權重字典
        """
        updated = {}
        
        # 1. 提升被選中圖像的 token 權重
        selections = feedback.get("selections", [])
        if selections:
            # 假設從歷史記錄中取得這些圖像使用的 token
            # 這裡簡化：統一提升主要 token
            for category in ["lighting", "material", "composition"]:
                if category in self.weights:
                    for token in list(self.weights[category].keys())[:2]:
                        old_weight = self.weights[category][token]
                        new_weight = min(old_weight + 0.05, 2.0)
                        self.weights[category][token] = new_weight
                        updated[f"{category}.{token}"] = new_weight
        
        # 2. 根據標籤插入補救 token
        tags = feedback.get("tags", {})
        for img_id, tag_list in tags.items():
            for tag in tag_list:
                adjustment = self._tag_to_adjustment(tag)
                if adjustment:
                    for token, delta in adjustment.items():
                        cat, tok = token.split(".", 1)
                        if cat in self.weights and tok in self.weights[cat]:
                            old = self.weights[cat][tok]
                            new = max(0.5, min(old + delta, 2.0))
                            self.weights[cat][tok] = new
                            updated[token] = new
        
        # 儲存更新後的權重
        self._save_weights()
        
        logger.info(f"已更新 {len(updated)} 個權重")
        return updated
    
    def _tag_to_adjustment(self, tag: str) -> Optional[Dict[str, float]]:
        """標籤 → 權重調整映射"""
        adjustments = {
            "lighting too flat": {
                "lighting.dramatic rim light": +0.15,
                "lighting.high contrast": +0.10
            },
            "background cluttered": {
                "composition.shallow depth of field": +0.10,
                "detail.intricate": -0.10
            },
            "color too vibrant": {
                "atmosphere.vibrant": -0.15
            },
            "lacks detail": {
                "detail.ultra detailed": +0.10,
                "material.intricate": +0.10
            }
        }
        return adjustments.get(tag)
    
    def _save_weights(self):
        """儲存權重表"""
        with open(self.weights_path, 'w', encoding='utf-8') as f:
            json.dump(self.weights, f, indent=2, ensure_ascii=False)
        logger.info(f"權重表已儲存至 {self.weights_path}")
    
    def generate_variations(
        self,
        base_prompt: str,
        count: int = 4
    ) -> List[str]:
        """
        從基礎 Prompt 生成變體
        
        Args:
            base_prompt: 基礎 Prompt
            count: 變體數量
        
        Returns:
            Prompt 變體列表
        """
        variations = [base_prompt]
        
        # 變體策略：調整光線、角度、細節
        variation_modifiers = [
            ", dramatic side lighting, high contrast",
            ", soft ambient glow, ethereal atmosphere",
            ", close-up composition, shallow depth of field",
            ", wide angle perspective, expansive view",
            ", top-down view, symmetrical composition",
            ", low angle shot, heroic perspective"
        ]
        
        for i in range(1, count):
            if i - 1 < len(variation_modifiers):
                variations.append(base_prompt + variation_modifiers[i - 1])
            else:
                # 隨機組合
                mod = random.choice(variation_modifiers)
                variations.append(base_prompt + mod)
        
        return variations[:count]


# ========== 測試用例 ==========
if __name__ == "__main__":
    engine = PromptEngine()
    
    # 測試組合 Prompt
    prompt, neg = engine.compose_prompt(
        theme="東方龍與財富",
        style_keywords=["cinematic", "volumetric light"],
        color_hex=["#B30012", "#CFA64D"],
        ratio="16:9"
    )
    
    print("=== Positive Prompt ===")
    print(prompt)
    print("\n=== Negative Prompt ===")
    print(neg)
    
    # 測試生成變體
    print("\n=== Variations ===")
    variations = engine.generate_variations(prompt, count=3)
    for i, var in enumerate(variations, 1):
        print(f"\n變體 {i}:")
        print(var)
