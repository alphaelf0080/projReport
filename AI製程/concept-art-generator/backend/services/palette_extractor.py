"""
色板提取器
從參考圖中提取主色調並轉換為 HEX 色碼
"""
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from typing import List, Tuple, Optional
from io import BytesIO
import requests
from loguru import logger


class PaletteExtractor:
    """色板提取與分析"""
    
    def __init__(self, n_colors: int = 6):
        """
        初始化提取器
        
        Args:
            n_colors: 要提取的色彩數量（預設 6）
        """
        self.n_colors = n_colors
    
    def extract_from_url(self, image_url: str) -> List[str]:
        """
        從圖片 URL 提取色板
        
        Args:
            image_url: 圖片 URL
        
        Returns:
            HEX 色碼列表
        """
        try:
            # 下載圖片
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # 開啟圖片
            image = Image.open(BytesIO(response.content))
            return self.extract_from_image(image)
        
        except Exception as e:
            logger.error(f"從 URL 提取色板失敗: {e}")
            return []
    
    def extract_from_bytes(self, image_bytes: bytes) -> dict:
        """
        從圖片位元組提取色板（用於上傳檔案）
        
        Args:
            image_bytes: 圖片位元組資料
        
        Returns:
            包含色彩資訊的字典
        """
        try:
            # 開啟圖片
            image = Image.open(BytesIO(image_bytes))
            hex_colors = self.extract_from_image(image)
            
            # 構建完整的色板資訊
            colors_info = []
            total_colors = len(hex_colors)
            
            for i, hex_color in enumerate(hex_colors):
                rgb = self._hex_to_rgb(hex_color)
                color_name = self._rgb_to_color_name(rgb)
                
                # 計算比例（依序遞減）
                percentage = (total_colors - i) / sum(range(1, total_colors + 1))
                
                colors_info.append({
                    "hex": hex_color,
                    "name": color_name,
                    "rgb": rgb,
                    "percentage": round(percentage, 3)
                })
            
            # 分類顏色
            palette = {
                "colors": colors_info,
                "primary": [colors_info[0]["hex"]] if colors_info else [],
                "secondary": [c["hex"] for c in colors_info[1:3]] if len(colors_info) > 1 else [],
                "accent": [c["hex"] for c in colors_info[3:]] if len(colors_info) > 3 else []
            }
            
            logger.info(f"從位元組提取色板: {len(colors_info)} 種顏色")
            return palette
            
        except Exception as e:
            logger.error(f"從位元組提取色板失敗: {e}")
            return {
                "colors": [],
                "primary": [],
                "secondary": [],
                "accent": []
            }
    
    def extract_from_image(self, image: Image.Image) -> List[str]:
        """
        從 PIL Image 提取色板
        
        Args:
            image: PIL Image 物件
        
        Returns:
            HEX 色碼列表（依重要性排序）
        """
        try:
            # 轉換為 RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 縮小圖片以加速處理（最大 300px）
            image.thumbnail((300, 300))
            
            # 轉為 numpy array
            pixels = np.array(image).reshape(-1, 3)
            
            # 過濾極端值（太暗或太亮）
            pixels = self._filter_extreme_colors(pixels)
            
            # K-means 聚類
            kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # 取得聚類中心（主色）
            colors = kmeans.cluster_centers_.astype(int)
            
            # 計算每個聚類的樣本數（作為重要性）
            labels = kmeans.labels_
            counts = np.bincount(labels)
            
            # 依重要性排序
            sorted_indices = np.argsort(counts)[::-1]
            sorted_colors = colors[sorted_indices]
            
            # 轉換為 HEX
            hex_colors = [self._rgb_to_hex(color) for color in sorted_colors]
            
            # 去除相似色（ΔE < 閾值）
            hex_colors = self._remove_similar_colors(hex_colors, threshold=20)
            
            logger.info(f"成功提取 {len(hex_colors)} 個主色")
            return hex_colors
        
        except Exception as e:
            logger.error(f"提取色板失敗: {e}")
            return []
    
    def _filter_extreme_colors(
        self,
        pixels: np.ndarray,
        min_brightness: int = 20,
        max_brightness: int = 240
    ) -> np.ndarray:
        """
        過濾過暗或過亮的像素
        
        Args:
            pixels: RGB 像素陣列 (N, 3)
            min_brightness: 最小亮度
            max_brightness: 最大亮度
        
        Returns:
            過濾後的像素陣列
        """
        # 計算亮度（簡化：平均 RGB）
        brightness = pixels.mean(axis=1)
        
        # 過濾
        mask = (brightness >= min_brightness) & (brightness <= max_brightness)
        filtered = pixels[mask]
        
        # 如果過濾後太少，返回原始
        if len(filtered) < 100:
            return pixels
        
        return filtered
    
    def _rgb_to_hex(self, rgb: np.ndarray) -> str:
        """RGB 轉 HEX"""
        r, g, b = rgb
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """HEX 轉 RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _color_distance(self, rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
        """
        計算兩色彩之間的距離（簡化 ΔE）
        使用歐氏距離在 RGB 空間（實際應用可改用 Lab 空間）
        """
        return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))
    
    def _remove_similar_colors(
        self,
        hex_colors: List[str],
        threshold: float = 20.0
    ) -> List[str]:
        """
        移除過於相似的顏色
        
        Args:
            hex_colors: HEX 色碼列表
            threshold: 相似度閾值（ΔE）
        
        Returns:
            去重後的 HEX 列表
        """
        if len(hex_colors) <= 1:
            return hex_colors
        
        unique_colors = [hex_colors[0]]
        
        for hex_color in hex_colors[1:]:
            rgb = self._hex_to_rgb(hex_color)
            
            # 檢查是否與已選顏色過於相似
            is_similar = False
            for unique_hex in unique_colors:
                unique_rgb = self._hex_to_rgb(unique_hex)
                distance = self._color_distance(rgb, unique_rgb)
                
                if distance < threshold:
                    is_similar = True
                    break
            
            if not is_similar:
                unique_colors.append(hex_color)
        
        return unique_colors
    
    def categorize_colors(
        self,
        hex_colors: List[str]
    ) -> dict:
        """
        將顏色分類為主色/輔色/點綴色
        
        Args:
            hex_colors: HEX 色碼列表（已依重要性排序）
        
        Returns:
            分類後的字典 {"primary": [...], "secondary": [...], "accent": [...]}
        """
        n = len(hex_colors)
        
        if n == 0:
            return {"primary": [], "secondary": [], "accent": []}
        
        # 簡單分類：前 2 個主色，中間輔色，最後點綴色
        primary = hex_colors[:min(2, n)]
        secondary = hex_colors[2:min(4, n)] if n > 2 else []
        accent = hex_colors[4:] if n > 4 else []
        
        return {
            "primary": primary,
            "secondary": secondary,
            "accent": accent
        }
    
    def generate_palette_description(self, hex_colors: List[str]) -> str:
        """
        生成色板的文字描述（用於 Prompt）
        
        Args:
            hex_colors: HEX 色碼列表
        
        Returns:
            色彩描述字串
        """
        if not hex_colors:
            return ""
        
        # 將 HEX 轉為色彩名稱
        color_names = []
        for hex_code in hex_colors[:3]:  # 最多 3 個
            rgb = self._hex_to_rgb(hex_code)
            name = self._rgb_to_color_name(rgb)
            if name:
                color_names.append(name)
        
        if not color_names:
            return ""
        
        if len(color_names) == 1:
            return f"{color_names[0]} palette"
        elif len(color_names) == 2:
            return f"{color_names[0]} and {color_names[1]} palette"
        else:
            return f"{', '.join(color_names[:-1])} and {color_names[-1]} palette"
    
    def _rgb_to_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """RGB 轉色彩名稱（簡化映射）"""
        r, g, b = rgb
        
        # 判斷主導色
        max_channel = max(r, g, b)
        min_channel = min(r, g, b)
        
        # 飽和度
        saturation = (max_channel - min_channel) / max_channel if max_channel > 0 else 0
        
        # 亮度
        brightness = (r + g + b) / 3
        
        # 低飽和度 → 中性色
        if saturation < 0.2:
            if brightness < 50:
                return "dark neutral"
            elif brightness > 200:
                return "light neutral"
            else:
                return "gray"
        
        # 高飽和度 → 色相判斷
        if r > g and r > b:
            # 紅色系
            if r > 200:
                return "crimson" if r > g + 50 else "coral"
            else:
                return "burgundy"
        
        elif g > r and g > b:
            # 綠色系
            if g > 200:
                return "emerald" if g > r + 50 else "lime"
            else:
                return "forest green"
        
        elif b > r and b > g:
            # 藍色系
            if b > 200:
                return "sapphire" if b > g + 50 else "sky blue"
            else:
                return "navy"
        
        elif r > 180 and g > 150:
            # 黃/金色系
            if r > 220 and g > 180:
                return "golden"
            else:
                return "amber"
        
        elif r > 150 and b > 150:
            # 紫/洋紅系
            return "violet" if b > r + 30 else "magenta"
        
        else:
            return "mixed"


# ========== 測試用例 ==========
if __name__ == "__main__":
    extractor = PaletteExtractor(n_colors=6)
    
    # 測試：從本地圖片提取
    # image = Image.open("test_image.jpg")
    # hex_colors = extractor.extract_from_image(image)
    
    # 測試：生成測試圖片
    test_colors = [
        (179, 0, 18),    # 深紅
        (207, 166, 77),  # 金色
        (255, 215, 0),   # 金黃
        (50, 50, 50)     # 深灰
    ]
    
    # 建立測試圖片
    width, height = 200, 200
    test_img = Image.new('RGB', (width, height))
    pixels = test_img.load()
    
    for y in range(height):
        for x in range(width):
            color_idx = (x // 50 + y // 50) % len(test_colors)
            pixels[x, y] = test_colors[color_idx]
    
    # 提取色板
    hex_colors = extractor.extract_from_image(test_img)
    
    print("=== 提取的色板 ===")
    for i, hex_code in enumerate(hex_colors, 1):
        print(f"{i}. {hex_code}")
    
    # 分類
    categorized = extractor.categorize_colors(hex_colors)
    print("\n=== 色彩分類 ===")
    print(f"主色: {categorized['primary']}")
    print(f"輔色: {categorized['secondary']}")
    print(f"點綴色: {categorized['accent']}")
    
    # 生成描述
    description = extractor.generate_palette_description(hex_colors)
    print(f"\n=== 色彩描述 ===")
    print(description)
