"""
資料模型定義
定義所有 API 的請求與回應結構
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class AspectRatio(str, Enum):
    """支援的圖像比例"""
    LANDSCAPE = "16:9"
    PORTRAIT = "4:5"
    SQUARE = "1:1"
    ULTRA_WIDE = "21:9"


class GenerationStatus(str, Enum):
    """生成任務狀態"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ========== 輸入結構 ==========

class ColorPreferences(BaseModel):
    """色彩偏好"""
    primary: List[str] = Field(
        description="主色調 HEX 列表",
        example=["#B30012", "#D41F27"]
    )
    secondary: List[str] = Field(
        default=[],
        description="輔色 HEX 列表",
        example=["#CFA64D", "#F7E09A"]
    )
    mood: Optional[str] = Field(
        default=None,
        description="色彩情緒描述",
        example="尊貴 能量 幸運"
    )


class ReferenceImage(BaseModel):
    """參考圖片"""
    id: str = Field(description="參考圖 ID")
    url: str = Field(description="圖片 URL 或 Base64")
    tags: List[str] = Field(default=[], description="人工標籤")
    weight: float = Field(default=1.0, ge=0.0, le=2.0, description="影響權重")


class BriefIn(BaseModel):
    """創意簡報輸入"""
    theme: str = Field(
        description="遊戲主題",
        example="東方龍與財富"
    )
    styleKeywords: List[str] = Field(
        description="風格關鍵詞",
        example=["cinematic", "volumetric light", "golden accents"]
    )
    colorPreferences: ColorPreferences
    referenceImages: List[ReferenceImage] = Field(default=[])
    targetCount: int = Field(default=4, ge=1, le=10, description="目標生成數量")
    targetRatio: AspectRatio = Field(default=AspectRatio.LANDSCAPE)
    constraints: Optional[Dict[str, bool]] = Field(
        default=None,
        description="內容限制",
        example={"violence": False, "religiousSymbols": False}
    )


class GenerateRequest(BaseModel):
    """圖像生成請求"""
    briefId: str = Field(description="關聯的 Brief ID")
    count: int = Field(default=4, ge=1, le=10, description="生成數量")
    ratio: AspectRatio = Field(default=AspectRatio.LANDSCAPE)
    seed: Optional[int] = Field(default=None, description="固定隨機種子")
    variations: Optional[List[str]] = Field(
        default=None,
        description="變體要求",
        example=["close-up", "wide angle", "top view"]
    )


class FeedbackIn(BaseModel):
    """美術師反饋"""
    generationId: str = Field(description="生成任務 ID")
    selections: List[str] = Field(
        description="選中的圖片 ID",
        example=["img_b.png", "img_d.png"]
    )
    ratings: Dict[str, int] = Field(
        description="圖片評分 (1-5)",
        example={"img_b.png": 5, "img_d.png": 4}
    )
    tags: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="問題標籤",
        example={"img_a.png": ["lighting too flat", "background cluttered"]}
    )
    adjustments: List[str] = Field(
        default=[],
        description="調整建議",
        example=["增強龍鱗立體感", "背景雲霧降低飽和度 20%"]
    )


# ========== 輸出結構 ==========

class BriefOut(BaseModel):
    """創意簡報回應"""
    briefId: str
    status: str = "created"
    theme: str
    styleTokens: List[str] = Field(description="提取的風格 Token")
    extractedPalette: Optional[List[str]] = Field(
        default=None,
        description="從參考圖提取的色板"
    )
    estimatedTime: int = Field(description="預估生成時間（秒）")
    createdAt: datetime


class GeneratedImage(BaseModel):
    """單張生成圖片資訊"""
    id: str
    url: str
    thumbnailUrl: str
    prompt: str
    seed: int
    size: Dict[str, int] = Field(example={"width": 1024, "height": 576})


class GenerationOut(BaseModel):
    """生成任務回應"""
    generationId: str
    briefId: str
    status: GenerationStatus
    images: List[GeneratedImage] = []
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    message: Optional[str] = None
    createdAt: datetime
    completedAt: Optional[datetime] = None


class FeedbackOut(BaseModel):
    """反饋處理回應"""
    ok: bool
    message: str
    updatedWeights: Dict[str, float] = Field(
        description="更新後的 Token 權重"
    )
    suggestedAdjustments: List[str] = Field(
        description="系統建議的調整方向"
    )


# ========== 內部資料結構 ==========

class PromptLog(BaseModel):
    """Prompt 記錄"""
    id: str
    briefId: str
    basePrompt: str
    negativePrompt: str
    styleTokens: List[str]
    seed: int
    modelInfo: Dict[str, str] = Field(
        example={"name": "SDXL_base", "version": "1.0"}
    )
    parameters: Dict[str, any] = Field(
        example={"steps": 40, "cfg_scale": 7.0}
    )
    outputIds: List[str]
    createdAt: datetime


class TokenWeight(BaseModel):
    """Token 權重"""
    token: str
    weight: float = Field(default=1.0, ge=0.0, le=2.0)
    category: str = Field(
        description="分類",
        example="lighting"
    )
    lastUpdated: datetime


class StyleTokenDatabase(BaseModel):
    """風格 Token 資料庫"""
    lighting: Dict[str, float]
    material: Dict[str, float]
    composition: Dict[str, float]
    atmosphere: Dict[str, float]
    detail: Dict[str, float]


# ========== 錯誤回應 ==========

class ErrorResponse(BaseModel):
    """錯誤回應"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
