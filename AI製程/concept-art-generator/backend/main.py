"""
FastAPI 主程式
提供 REST API 端點供前端調用
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
import uuid
from pathlib import Path
from typing import Dict
from loguru import logger

# 匯入自訂模組
from models.schemas import (
    BriefIn, BriefOut, GenerateRequest, GenerationOut,
    FeedbackIn, FeedbackOut, GeneratedImage, GenerationStatus
)
from services.prompt_engine import PromptEngine
from services.palette_extractor import PaletteExtractor
from services.image_generator import ImageGenerator


# ========== 初始化 ==========
app = FastAPI(
    title="Slot Game Concept Art Generator API",
    description="互動式 AI 工具，快速生成 Slot Game Concept Art",
    version="1.0.0"
)

# CORS 設定（允許前端跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應限制來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 靜態檔案服務（輸出圖像）
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")

# 初始化服務
prompt_engine = PromptEngine()
palette_extractor = PaletteExtractor()
image_generator = ImageGenerator()  # 延遲載入模型

# 簡易記憶體儲存（生產環境應使用資料庫）
briefs_db: Dict[str, dict] = {}
generations_db: Dict[str, dict] = {}

logger.info("API 服務已啟動")


# ========== API 端點 ==========

@app.get("/")
def read_root():
    """根路徑"""
    return {
        "service": "Slot Game Concept Art Generator",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "brief": "/api/brief",
            "generate": "/api/generate",
            "feedback": "/api/feedback",
            "docs": "/docs"
        }
    }


@app.post("/api/brief", response_model=BriefOut)
def create_brief(brief: BriefIn):
    """
    建立創意簡報
    
    處理流程:
    1. 提取風格 token
    2. 從參考圖提取色板
    3. 生成初始 prompt
    4. 儲存 brief
    """
    try:
        brief_id = f"brief_{uuid.uuid4().hex[:8]}"
        
        # 1. 提取風格 token（簡化版：直接使用關鍵詞）
        style_tokens = brief.styleKeywords
        
        # 2. 從參考圖提取色板
        extracted_palette = []
        if brief.referenceImages:
            logger.info(f"處理 {len(brief.referenceImages)} 張參考圖")
            for ref in brief.referenceImages[:2]:  # 限制處理 2 張
                try:
                    colors = palette_extractor.extract_from_url(ref.url)
                    extracted_palette.extend(colors)
                except Exception as e:
                    logger.warning(f"參考圖處理失敗: {e}")
        
        # 去重並限制數量
        extracted_palette = list(set(extracted_palette))[:6]
        
        # 3. 合併使用者提供與提取的色板
        all_colors = brief.colorPreferences.primary + brief.colorPreferences.secondary
        if extracted_palette:
            all_colors.extend(extracted_palette)
        all_colors = list(set(all_colors))[:8]
        
        # 4. 生成初始 prompt（用於預覽）
        preview_prompt, _ = prompt_engine.compose_prompt(
            theme=brief.theme,
            style_keywords=style_tokens,
            color_hex=all_colors,
            ratio=brief.targetRatio.value
        )
        
        # 5. 預估時間（每張約 10 秒）
        estimated_time = brief.targetCount * 10
        
        # 6. 儲存 brief
        brief_data = {
            "briefId": brief_id,
            "input": brief.dict(),
            "styleTokens": style_tokens,
            "extractedPalette": extracted_palette,
            "allColors": all_colors,
            "previewPrompt": preview_prompt,
            "estimatedTime": estimated_time,
            "createdAt": datetime.now()
        }
        briefs_db[brief_id] = brief_data
        
        logger.info(f"已建立 Brief: {brief_id}")
        
        return BriefOut(
            briefId=brief_id,
            status="created",
            theme=brief.theme,
            styleTokens=style_tokens,
            extractedPalette=extracted_palette if extracted_palette else None,
            estimatedTime=estimated_time,
            createdAt=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"建立 Brief 失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate", response_model=GenerationOut)
def generate_images(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    生成圖像
    
    處理流程:
    1. 查詢 brief
    2. 組合 prompt
    3. 生成圖像（背景任務）
    4. 回傳任務 ID
    """
    try:
        # 1. 查詢 brief
        if request.briefId not in briefs_db:
            raise HTTPException(status_code=404, detail="Brief 不存在")
        
        brief_data = briefs_db[request.briefId]
        generation_id = f"gen_{uuid.uuid4().hex[:8]}"
        
        # 2. 組合 prompt
        base_prompt, negative_prompt = prompt_engine.compose_prompt(
            theme=brief_data["input"]["theme"],
            style_keywords=brief_data["styleTokens"],
            color_hex=brief_data["allColors"],
            ratio=request.ratio.value
        )
        
        # 3. 生成變體 prompt
        if request.variations:
            # 根據變體要求調整
            prompts = []
            for var in request.variations[:request.count]:
                var_prompt, _ = prompt_engine.compose_prompt(
                    theme=brief_data["input"]["theme"],
                    style_keywords=brief_data["styleTokens"],
                    color_hex=brief_data["allColors"],
                    ratio=request.ratio.value,
                    variation=var
                )
                prompts.append(var_prompt)
        else:
            prompts = prompt_engine.generate_variations(base_prompt, count=request.count)
        
        # 4. 初始化生成任務
        gen_data = {
            "generationId": generation_id,
            "briefId": request.briefId,
            "status": GenerationStatus.QUEUED,
            "prompts": prompts,
            "negativePrompt": negative_prompt,
            "seed": request.seed,
            "ratio": request.ratio.value,
            "images": [],
            "createdAt": datetime.now()
        }
        generations_db[generation_id] = gen_data
        
        # 5. 啟動背景任務生成圖像
        background_tasks.add_task(
            generate_images_task,
            generation_id=generation_id,
            prompts=prompts,
            negative_prompt=negative_prompt,
            seed=request.seed,
            ratio=request.ratio.value
        )
        
        logger.info(f"已建立生成任務: {generation_id}")
        
        return GenerationOut(
            generationId=generation_id,
            briefId=request.briefId,
            status=GenerationStatus.QUEUED,
            images=[],
            progress=0,
            message="任務已加入佇列",
            createdAt=datetime.now()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"建立生成任務失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def generate_images_task(
    generation_id: str,
    prompts: list,
    negative_prompt: str,
    seed: int,
    ratio: str
):
    """背景任務：執行圖像生成"""
    try:
        # 更新狀態
        generations_db[generation_id]["status"] = GenerationStatus.PROCESSING
        generations_db[generation_id]["progress"] = 10
        
        logger.info(f"開始生成: {generation_id}")
        
        # 為每個 prompt 生成圖像
        all_images = []
        for i, prompt in enumerate(prompts):
            try:
                # 生成
                images = image_generator.generate(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    seed=seed + i if seed else None,
                    num_images=1,
                    ratio=ratio
                )
                
                # 儲存
                saved_paths = image_generator.save_images(
                    images,
                    prefix=f"{generation_id}"
                )
                
                # 建立縮圖
                for idx, (image, path) in enumerate(zip(images, saved_paths)):
                    thumb = image_generator.create_thumbnail(image)
                    thumb_path = Path(path).with_suffix('.thumb.png')
                    thumb.save(thumb_path)
                    
                    # 記錄圖像資訊
                    img_info = GeneratedImage(
                        id=f"{generation_id}_{chr(97+i+idx)}",
                        url=f"/output/{Path(path).name}",
                        thumbnailUrl=f"/output/{thumb_path.name}",
                        prompt=prompt,
                        seed=seed + i if seed else 0,
                        size={"width": image.width, "height": image.height}
                    )
                    all_images.append(img_info)
                
                # 更新進度
                progress = int((i + 1) / len(prompts) * 90) + 10
                generations_db[generation_id]["progress"] = progress
                
            except Exception as e:
                logger.error(f"生成圖像失敗 (prompt {i}): {e}")
        
        # 更新最終狀態
        generations_db[generation_id]["status"] = GenerationStatus.COMPLETED
        generations_db[generation_id]["progress"] = 100
        generations_db[generation_id]["images"] = all_images
        generations_db[generation_id]["completedAt"] = datetime.now()
        
        logger.info(f"生成完成: {generation_id}, 共 {len(all_images)} 張")
    
    except Exception as e:
        logger.error(f"生成任務失敗: {e}")
        generations_db[generation_id]["status"] = GenerationStatus.FAILED
        generations_db[generation_id]["message"] = str(e)


@app.get("/api/generation/{generation_id}", response_model=GenerationOut)
def get_generation(generation_id: str):
    """查詢生成任務狀態"""
    if generation_id not in generations_db:
        raise HTTPException(status_code=404, detail="生成任務不存在")
    
    gen_data = generations_db[generation_id]
    
    return GenerationOut(
        generationId=gen_data["generationId"],
        briefId=gen_data["briefId"],
        status=gen_data["status"],
        images=gen_data.get("images", []),
        progress=gen_data.get("progress"),
        message=gen_data.get("message"),
        createdAt=gen_data["createdAt"],
        completedAt=gen_data.get("completedAt")
    )


@app.post("/api/feedback", response_model=FeedbackOut)
def submit_feedback(feedback: FeedbackIn):
    """
    提交美術師反饋並更新權重
    """
    try:
        # 驗證 generation ID
        if feedback.generationId not in generations_db:
            raise HTTPException(status_code=404, detail="生成任務不存在")
        
        # 更新 token 權重
        updated_weights = prompt_engine.update_weights({
            "selections": feedback.selections,
            "ratings": feedback.ratings,
            "tags": feedback.tags
        })
        
        # 根據反饋生成建議
        suggestions = []
        if feedback.tags:
            for img_id, tag_list in feedback.tags.items():
                for tag in tag_list:
                    if "lighting" in tag:
                        suggestions.append("建議增強光線對比度")
                    elif "background" in tag:
                        suggestions.append("建議簡化背景元素")
                    elif "detail" in tag:
                        suggestions.append("建議調整細節層次")
        
        if not suggestions:
            suggestions.append("可繼續生成下一批變體")
        
        logger.info(f"已處理反饋: {feedback.generationId}")
        
        return FeedbackOut(
            ok=True,
            message="反饋已處理，權重已更新",
            updatedWeights=updated_weights,
            suggestedAdjustments=suggestions
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"處理反饋失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "briefs_count": len(briefs_db),
        "generations_count": len(generations_db)
    }


# ========== 啟動服務 ==========
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開發模式自動重載
        log_level="info"
    )
