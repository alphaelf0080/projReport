"""
圖像生成服務
使用 Stable Diffusion XL 生成圖像
"""
import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from PIL import Image
import random
from pathlib import Path
from typing import List, Optional, Dict
from loguru import logger
import time


class ImageGenerator:
    """AI 圖像生成器"""
    
    def __init__(
        self,
        model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
        device: str = "cuda",
        enable_xformers: bool = True
    ):
        """
        初始化生成器
        
        Args:
            model_id: Hugging Face 模型 ID
            device: 運行設備 (cuda/mps/cpu)
            enable_xformers: 是否啟用 xformers 記憶體優化
        """
        self.model_id = model_id
        self.device = self._get_device(device)
        self.pipe = None
        self.enable_xformers = enable_xformers
        
        # 預設生成參數
        self.default_params = {
            "num_inference_steps": 40,
            "guidance_scale": 7.0,
            "width": 1024,
            "height": 576  # 16:9
        }
        
        logger.info(f"初始化圖像生成器 (設備: {self.device})")
    
    def _get_device(self, preferred: str) -> str:
        """自動檢測可用設備"""
        if preferred == "cuda" and torch.cuda.is_available():
            return "cuda"
        elif preferred == "mps" and torch.backends.mps.is_available():
            return "mps"
        else:
            logger.warning("GPU 不可用，使用 CPU（速度較慢）")
            return "cpu"
    
    def load_model(self):
        """載入模型（首次調用時）"""
        if self.pipe is not None:
            logger.info("模型已載入")
            return
        
        logger.info(f"正在載入模型: {self.model_id}")
        start_time = time.time()
        
        try:
            # 載入 pipeline
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            
            # 優化排程器
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # 移至設備
            self.pipe = self.pipe.to(self.device)
            
            # 啟用記憶體優化
            if self.enable_xformers and self.device == "cuda":
                try:
                    self.pipe.enable_xformers_memory_efficient_attention()
                    logger.info("已啟用 xformers 優化")
                except Exception as e:
                    logger.warning(f"xformers 啟用失敗: {e}")
            
            # VAE 優化
            if self.device == "cuda":
                self.pipe.enable_vae_slicing()
                self.pipe.enable_vae_tiling()
            
            elapsed = time.time() - start_time
            logger.info(f"模型載入完成 (耗時: {elapsed:.1f}s)")
        
        except Exception as e:
            logger.error(f"模型載入失敗: {e}")
            raise
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        seed: Optional[int] = None,
        num_images: int = 1,
        ratio: str = "16:9",
        **kwargs
    ) -> List[Image.Image]:
        """
        生成圖像
        
        Args:
            prompt: 正面提示詞
            negative_prompt: 負面提示詞
            seed: 隨機種子（None 則隨機）
            num_images: 生成數量
            ratio: 圖像比例 (16:9, 4:5, 1:1)
            **kwargs: 其他參數覆蓋
        
        Returns:
            PIL Image 列表
        """
        # 確保模型已載入
        self.load_model()
        
        # 解析比例
        width, height = self._ratio_to_size(ratio)
        
        # 合併參數
        params = {**self.default_params, **kwargs}
        params["width"] = width
        params["height"] = height
        
        # 設定隨機種子
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        
        generator = torch.Generator(device=self.device).manual_seed(seed)
        
        logger.info(f"開始生成 {num_images} 張圖像 (seed: {seed})")
        start_time = time.time()
        
        try:
            # 批次生成
            images = self.pipe(
                prompt=[prompt] * num_images,
                negative_prompt=[negative_prompt] * num_images,
                generator=generator,
                num_inference_steps=params["num_inference_steps"],
                guidance_scale=params["guidance_scale"],
                width=params["width"],
                height=params["height"]
            ).images
            
            elapsed = time.time() - start_time
            logger.info(f"生成完成 (耗時: {elapsed:.1f}s, 平均: {elapsed/num_images:.1f}s/張)")
            
            return images
        
        except Exception as e:
            logger.error(f"生成失敗: {e}")
            raise
    
    def _ratio_to_size(self, ratio: str) -> tuple:
        """比例 → 尺寸轉換"""
        ratio_map = {
            "16:9": (1024, 576),
            "4:5": (832, 1024),
            "1:1": (1024, 1024),
            "21:9": (1344, 576)
        }
        return ratio_map.get(ratio, (1024, 576))
    
    def save_images(
        self,
        images: List[Image.Image],
        output_dir: str = "output",
        prefix: str = "gen"
    ) -> List[str]:
        """
        儲存圖像
        
        Args:
            images: PIL Image 列表
            output_dir: 輸出目錄
            prefix: 檔名前綴
        
        Returns:
            檔案路徑列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_paths = []
        timestamp = int(time.time())
        
        for i, image in enumerate(images):
            filename = f"{prefix}_{timestamp}_{chr(97+i)}.png"  # a, b, c...
            filepath = output_path / filename
            image.save(filepath, format="PNG", optimize=True)
            saved_paths.append(str(filepath))
            logger.info(f"已儲存: {filepath}")
        
        return saved_paths
    
    def create_thumbnail(
        self,
        image: Image.Image,
        size: tuple = (256, 256)
    ) -> Image.Image:
        """建立縮圖"""
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
    
    def unload_model(self):
        """卸載模型以釋放記憶體"""
        if self.pipe is not None:
            del self.pipe
            self.pipe = None
            
            if self.device == "cuda":
                torch.cuda.empty_cache()
            
            logger.info("模型已卸載")


# ========== 測試用例 ==========
if __name__ == "__main__":
    # 注意：首次執行會下載約 6GB 模型
    generator = ImageGenerator()
    
    # 測試提示詞
    prompt = (
        "Majestic oriental dragon coiling around luminous golden orb, "
        "flowing auspicious clouds, cinematic composition, "
        "dramatic rim light, volumetric light rays, "
        "intricate scales, ornate gold accents, "
        "rich crimson and imperial gold palette, "
        "premium slot game concept art, ultra detailed, 16:9"
    )
    
    negative_prompt = (
        "low quality, blurry, watermark, distorted, "
        "extra limbs, flat lighting, noisy background"
    )
    
    # 生成圖像
    images = generator.generate(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_images=2,
        seed=42
    )
    
    # 儲存
    saved_paths = generator.save_images(images, prefix="dragon_test")
    print(f"已生成 {len(saved_paths)} 張圖像")
    for path in saved_paths:
        print(f"  - {path}")
