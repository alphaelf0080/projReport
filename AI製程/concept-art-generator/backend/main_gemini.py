"""
FastAPI 應用 - Gemini 版本
使用 Google Gemini 作為對話式 AI 代理
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import asyncio
from loguru import logger
import os
from pathlib import Path

# 服務
from services.gemini_agent import GeminiConceptAgent, GeminiImageGenerator
from services.palette_extractor import PaletteExtractor

# 初始化
app = FastAPI(
    title="Slot Game Concept Art Generator (Gemini Edition)",
    description="使用 Google Gemini 的對話式 Concept Art 生成系統",
    version="2.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全域服務實例
gemini_agent: Optional[GeminiConceptAgent] = None
image_generator: Optional[GeminiImageGenerator] = None
palette_extractor = PaletteExtractor()

# 對話 Session 儲存
sessions: Dict[str, Dict[str, Any]] = {}

# ==================== 資料模型 ====================

class ChatMessage(BaseModel):
    """對話訊息"""
    session_id: Optional[str] = None
    message: str
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    """對話回應"""
    session_id: str
    response: str
    prompt_ready: bool
    prompt_data: Optional[Dict] = None
    timestamp: str

class GenerateRequest(BaseModel):
    """圖像生成請求"""
    session_id: str
    prompt: str
    negative_prompt: str = ""
    num_images: int = 4
    aspect_ratio: str = "16:9"

class GenerationResult(BaseModel):
    """生成結果"""
    generation_id: str
    status: str  # "processing", "completed", "failed"
    images: List[str] = []
    progress: int = 0
    error: Optional[str] = None

# ==================== 啟動事件 ====================

@app.on_event("startup")
async def startup_event():
    """應用啟動時初始化服務"""
    global gemini_agent, image_generator
    
    logger.info("🚀 啟動 Gemini Concept Art Generator")
    
    try:
        # 檢查 API Key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("⚠️  未設定 GEMINI_API_KEY，Gemini Agent 將無法使用")
            logger.info("請在 .env 檔案中設定: GEMINI_API_KEY=your_api_key")
        else:
            gemini_agent = GeminiConceptAgent(api_key)
            image_generator = GeminiImageGenerator(api_key)
            logger.info("✅ Gemini Agent 初始化成功")
            
    except Exception as e:
        logger.error(f"❌ 初始化失敗: {e}")

# ==================== API 端點 ====================

@app.get("/")
async def root():
    """根路徑"""
    return {
        "app": "Slot Game Concept Art Generator",
        "version": "2.0.0 (Gemini Edition)",
        "status": "running",
        "gemini_ready": gemini_agent is not None
    }

@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "gemini_agent": gemini_agent is not None,
        "image_generator": image_generator is not None,
        "active_sessions": len(sessions)
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    """
    與 Gemini Agent 對話
    
    流程：
    1. 美術人員描述需求
    2. Gemini 引導並收集細節
    3. 當資訊充足時，生成結構化 Prompt
    """
    if not gemini_agent:
        raise HTTPException(
            status_code=503,
            detail="Gemini Agent 尚未初始化，請設定 GEMINI_API_KEY"
        )
    
    try:
        # 獲取或創建 Session
        session_id = message.session_id or str(uuid.uuid4())
        
        if session_id not in sessions:
            sessions[session_id] = {
                "id": session_id,
                "created_at": datetime.now().isoformat(),
                "agent": GeminiConceptAgent(),  # 每個 session 獨立 agent
                "history": []
            }
        
        session = sessions[session_id]
        agent = session["agent"]
        
        # 發送訊息給 Gemini
        result = await agent.chat(message.message, message.context)
        
        # 儲存對話歷史
        session["history"].append({
            "role": "user",
            "content": message.message,
            "timestamp": datetime.now().isoformat()
        })
        session["history"].append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        # 如果 Prompt 準備好了，儲存到 session
        if result["prompt_ready"]:
            session["prompt_data"] = result["prompt_data"]
            logger.info(f"Session {session_id} Prompt 已準備")
        
        return ChatResponse(
            session_id=session_id,
            response=result["response"],
            prompt_ready=result["prompt_ready"],
            prompt_data=result["prompt_data"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"對話錯誤: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-reference")
async def upload_reference(
    session_id: str,
    file: UploadFile = File(...)
):
    """
    上傳參考圖並分析色板
    
    Returns:
        色板分析結果，可作為 context 傳給 chat
    """
    try:
        # 讀取圖片
        content = await file.read()
        
        # 提取色板
        palette = palette_extractor.extract_from_bytes(content)
        
        # 儲存到 session
        if session_id in sessions:
            sessions[session_id]["reference_palette"] = palette
        
        logger.info(f"Session {session_id} 參考圖色板: {len(palette.get('colors', []))} 種顏色")
        
        return {
            "session_id": session_id,
            "palette": palette,
            "message": "參考圖分析完成"
        }
        
    except Exception as e:
        logger.error(f"參考圖上傳錯誤: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate", response_model=GenerationResult)
async def generate_images(request: GenerateRequest):
    """
    生成圖像
    
    使用 session 中的 Prompt 或手動提供的 Prompt
    """
    if not image_generator:
        raise HTTPException(
            status_code=503,
            detail="Image Generator 尚未初始化"
        )
    
    try:
        # 獲取 Prompt（優先使用 session 中的）
        session = sessions.get(request.session_id)
        if session and "prompt_data" in session:
            prompt = session["prompt_data"]["prompt"]
            negative_prompt = session["prompt_data"].get("negative_prompt", "")
        else:
            prompt = request.prompt
            negative_prompt = request.negative_prompt
        
        # 創建生成任務
        generation_id = str(uuid.uuid4())
        
        # 啟動背景生成（實際應用中應使用任務佇列）
        asyncio.create_task(
            _background_generate(
                generation_id,
                prompt,
                negative_prompt,
                request.num_images,
                request.aspect_ratio
            )
        )
        
        return GenerationResult(
            generation_id=generation_id,
            status="processing",
            progress=0
        )
        
    except Exception as e:
        logger.error(f"生成請求錯誤: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 生成任務儲存
generation_tasks: Dict[str, GenerationResult] = {}

async def _background_generate(
    generation_id: str,
    prompt: str,
    negative_prompt: str,
    num_images: int,
    aspect_ratio: str
):
    """背景生成任務"""
    try:
        generation_tasks[generation_id] = GenerationResult(
            generation_id=generation_id,
            status="processing",
            progress=10
        )
        
        # 呼叫 Imagen API（或其他圖像生成服務）
        image_urls = await image_generator.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images=num_images,
            aspect_ratio=aspect_ratio
        )
        
        # 更新結果
        generation_tasks[generation_id] = GenerationResult(
            generation_id=generation_id,
            status="completed",
            images=image_urls,
            progress=100
        )
        
        logger.info(f"生成完成: {generation_id}, {len(image_urls)} 張圖像")
        
    except Exception as e:
        logger.error(f"生成失敗: {e}")
        generation_tasks[generation_id] = GenerationResult(
            generation_id=generation_id,
            status="failed",
            error=str(e),
            progress=0
        )

@app.get("/api/generation/{generation_id}", response_model=GenerationResult)
async def get_generation_status(generation_id: str):
    """查詢生成狀態"""
    if generation_id not in generation_tasks:
        raise HTTPException(status_code=404, detail="生成任務不存在")
    
    return generation_tasks[generation_id]

@app.post("/api/session/reset")
async def reset_session(session_id: str):
    """重置對話 Session"""
    if session_id in sessions:
        sessions[session_id]["agent"].reset_conversation()
        sessions[session_id]["history"] = []
        return {"message": "Session 已重置"}
    else:
        raise HTTPException(status_code=404, detail="Session 不存在")

@app.get("/api/session/{session_id}/history")
async def get_session_history(session_id: str):
    """獲取對話歷史"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session 不存在")
    
    return {
        "session_id": session_id,
        "history": sessions[session_id]["history"]
    }

# ==================== WebSocket（即時對話）====================

@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """
    WebSocket 即時對話
    
    使用方式：
    前端連接 ws://localhost:8000/ws/chat/{session_id}
    發送 JSON: {"message": "你的訊息"}
    接收 JSON: {"response": "AI 回應", "prompt_ready": false}
    """
    await websocket.accept()
    logger.info(f"WebSocket 連線: {session_id}")
    
    # 獲取或創建 session
    if session_id not in sessions:
        sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "agent": GeminiConceptAgent(),
            "history": []
        }
    
    session = sessions[session_id]
    agent = session["agent"]
    
    try:
        while True:
            # 接收訊息
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            
            if not user_message:
                continue
            
            # 發送給 Gemini
            result = await agent.chat(user_message, data.get("context"))
            
            # 回傳結果
            await websocket.send_json({
                "response": result["response"],
                "prompt_ready": result["prompt_ready"],
                "prompt_data": result["prompt_data"],
                "timestamp": datetime.now().isoformat()
            })
            
            # 儲存歷史
            session["history"].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            session["history"].append({
                "role": "assistant",
                "content": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket 斷線: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket 錯誤: {e}")
        await websocket.close()

# ==================== 啟動服務 ====================

if __name__ == "__main__":
    import uvicorn
    import socket
    
    # 載入環境變數
    from dotenv import load_dotenv
    load_dotenv()
    
    # 獲取網路資訊
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "無法取得"
    
    # 顯示啟動資訊
    logger.info("=" * 70)
    logger.info("🚀 啟動 Gemini Concept Art Generator")
    logger.info("=" * 70)
    logger.info(f"主機名稱: {hostname}")
    logger.info(f"本機 IP:  {local_ip}")
    logger.info(f"綁定介面: 0.0.0.0 (所有網路介面)")
    logger.info(f"監聽端口: 3010")
    logger.info("=" * 70)
    logger.info(f"📍 本機訪問: http://localhost:3010")
    logger.info(f"📍 區網訪問: http://{local_ip}:3010")
    logger.info(f"📍 健康檢查: http://{local_ip}:3010/api/health")
    logger.info("=" * 70)
    logger.info("💡 遠端連線注意事項：")
    logger.info("   1. 確認防火牆已開啟 port 3010")
    logger.info("   2. 執行以下命令添加防火牆規則 (需管理員權限)：")
    logger.info("      netsh advfirewall firewall add rule name=\"Backend 3010\" dir=in action=allow protocol=TCP localport=3010")
    logger.info("   3. 前端配置使用: http://{}:3010".format(local_ip))
    logger.info("=" * 70)
    
    # 啟動服務
    uvicorn.run(
        "main_gemini:app",
        host="0.0.0.0",
        port=3010,
        reload=True,
        log_level="info"
    )
