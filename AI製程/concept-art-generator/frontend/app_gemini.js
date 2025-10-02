/**
 * Gemini 版本前端應用
 * 對話式 Concept Art 生成系統
 */

// 配置
const API_BASE = 'http://localhost:8000';
let sessionId = null;
let currentPromptData = null;
let ws = null;

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Gemini Concept Art Generator 初始化');
    
    // 創建新 Session
    sessionId = generateUUID();
    console.log(`Session ID: ${sessionId}`);
    
    // 初始化 WebSocket 連線（可選）
    // initWebSocket();
    
    // 設定事件監聽
    setupEventListeners();
    
    // 檢查後端狀態
    checkBackendHealth();
});

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// ==================== 事件監聽 ====================

function setupEventListeners() {
    // 移除 Enter 鍵自動發送功能
    // 使用者必須點擊按鈕才能發送訊息
    // Shift+Enter 仍可換行
    document.getElementById('chatInput').addEventListener('keydown', (e) => {
        // 不做任何處理，保留預設的換行行為
    });
    
    // 檔案上傳
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadReferenceImage(e.target.files[0]);
        }
    });
    
    // 拖放上傳
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            uploadReferenceImage(e.dataTransfer.files[0]);
        }
    });
}

// ==================== 後端通訊 ====================

async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();
        
        if (data.gemini_agent) {
            updateStatus('Gemini 已連線', 'success');
        } else {
            updateStatus('Gemini 未連線，請設定 API Key', 'warning');
            addSystemMessage('⚠️ 後端 Gemini Agent 未初始化，請確認已設定 GEMINI_API_KEY 環境變數');
        }
    } catch (error) {
        console.error('健康檢查失敗:', error);
        updateStatus('後端連線失敗', 'error');
        addSystemMessage('❌ 無法連線到後端服務，請確認後端已啟動');
    }
}

function updateStatus(text, type = 'success') {
    const statusText = document.getElementById('status-text');
    statusText.textContent = text;
    
    const statusDot = document.querySelector('.status-dot');
    statusDot.style.background = type === 'success' ? '#4CAF50' : 
                                 type === 'warning' ? '#FF9800' : 
                                 '#F44336';
}

// ==================== 發送訊息 ====================

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 清空輸入框
    input.value = '';
    
    // 顯示使用者訊息
    addMessage('user', message);
    
    // 禁用發送按鈕
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span class="loading"></span>';
    
    try {
        // 呼叫 API
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        // 顯示 AI 回應
        addMessage('assistant', data.response, data.prompt_ready);
        
        // 如果 Prompt 準備好了
        if (data.prompt_ready && data.prompt_data) {
            currentPromptData = data.prompt_data;
            updatePromptPreview(data.prompt_data);
            document.getElementById('generateBtn').disabled = false;
        }
        
    } catch (error) {
        console.error('發送訊息失敗:', error);
        addSystemMessage(`❌ 發送失敗: ${error.message}`);
    } finally {
        // 重新啟用發送按鈕
        sendBtn.disabled = false;
        sendBtn.innerHTML = '發送 📤';
    }
}

// ==================== 訊息顯示 ====================

function addMessage(role, content, promptReady = false) {
    const messagesDiv = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // 處理換行
    const formattedContent = content.replace(/\n/g, '<br>');
    contentDiv.innerHTML = formattedContent;
    
    // 如果 Prompt 準備好了，顯示徽章
    if (promptReady) {
        const badge = document.createElement('div');
        badge.className = 'prompt-ready-badge';
        badge.textContent = '✅ Prompt 已準備';
        contentDiv.appendChild(badge);
    }
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString('zh-TW');
    contentDiv.appendChild(timeDiv);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    messagesDiv.appendChild(messageDiv);
    
    // 滾動到底部
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addSystemMessage(text) {
    const messagesDiv = document.getElementById('chatMessages');
    
    const systemDiv = document.createElement('div');
    systemDiv.style.cssText = `
        text-align: center;
        padding: 0.5rem;
        margin: 1rem 0;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        font-size: 0.9rem;
        color: #888;
    `;
    systemDiv.textContent = text;
    
    messagesDiv.appendChild(systemDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ==================== 參考圖上傳 ====================

async function uploadReferenceImage(file) {
    console.log('上傳參考圖:', file.name);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);
    
    try {
        updateStatus('分析參考圖...', 'warning');
        
        // 先顯示縮圖預覽
        displayImagePreview(file);
        
        const response = await fetch(`${API_BASE}/api/upload-reference?session_id=${sessionId}`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        // 顯示色板
        displayColorPalette(data.palette);
        
        // 通知 AI
        addSystemMessage('✅ 參考圖已上傳並分析色板');
        
        // 自動發送訊息給 AI
        setTimeout(() => {
            document.getElementById('chatInput').value = 
                `我上傳了一張參考圖，已提取到色板。請根據這些顏色給我建議。`;
            sendMessage();
        }, 500);
        
        updateStatus('Gemini 已連線', 'success');
        
    } catch (error) {
        console.error('上傳失敗:', error);
        addSystemMessage(`❌ 上傳失敗: ${error.message}`);
        updateStatus('上傳失敗', 'error');
    }
}

function displayImagePreview(file) {
    const uploadArea = document.getElementById('uploadArea');
    
    // 創建圖片預覽容器
    const previewContainer = document.createElement('div');
    previewContainer.style.cssText = `
        position: relative;
        margin-top: 1rem;
    `;
    
    // 創建縮圖
    const img = document.createElement('img');
    img.style.cssText = `
        width: 100%;
        height: auto;
        max-height: 200px;
        object-fit: cover;
        border-radius: 8px;
        border: 2px solid rgba(255, 215, 0, 0.3);
    `;
    
    // 創建刪除按鈕
    const removeBtn = document.createElement('button');
    removeBtn.innerHTML = '✕';
    removeBtn.style.cssText = `
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        border: none;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        cursor: pointer;
        font-size: 14px;
        line-height: 1;
        transition: all 0.3s;
    `;
    removeBtn.title = '移除圖片';
    removeBtn.onclick = () => {
        previewContainer.remove();
        // 清空 file input
        document.getElementById('fileInput').value = '';
    };
    
    // 讀取並顯示圖片
    const reader = new FileReader();
    reader.onload = (e) => {
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    previewContainer.appendChild(img);
    previewContainer.appendChild(removeBtn);
    
    // 移除舊的預覽（如果有）
    const oldPreview = uploadArea.querySelector('div[style*="position: relative"]');
    if (oldPreview) {
        oldPreview.remove();
    }
    
    uploadArea.appendChild(previewContainer);
}

function displayColorPalette(palette) {
    const paletteDiv = document.getElementById('colorPalette');
    paletteDiv.innerHTML = '';
    paletteDiv.style.display = 'grid';
    
    const colors = palette.colors || [];
    
    colors.slice(0, 8).forEach(color => {
        const swatch = document.createElement('div');
        swatch.className = 'color-swatch';
        swatch.style.background = color.hex;
        swatch.setAttribute('data-color', color.hex);
        swatch.title = `${color.name || color.hex}\n比例: ${(color.percentage * 100).toFixed(1)}%`;
        paletteDiv.appendChild(swatch);
    });
}

// ==================== 快速提示 ====================

function useQuickPrompt(button) {
    const text = button.textContent.trim();
    const input = document.getElementById('chatInput');
    
    // 提取主題描述（移除 emoji）
    const theme = text.replace(/[^\u4e00-\u9fa5\w\s-]/g, '').trim();
    
    input.value = `我想做一個「${theme}」主題的 Slot Game`;
    input.focus();
}

// ==================== Prompt 預覽 ====================

function updatePromptPreview(promptData) {
    const previewDiv = document.getElementById('promptPreview');
    
    const theme = promptData.theme || '未設定';
    const style = (promptData.style_tags || []).join(', ') || '未設定';
    
    previewDiv.innerHTML = `
        <div style="color: #FFD700; font-weight: 600; margin-bottom: 0.5rem;">
            ✅ Prompt 已準備就緒
        </div>
        <div style="margin-bottom: 0.3rem;">
            <strong>主題:</strong> ${theme}
        </div>
        <div style="margin-bottom: 0.3rem;">
            <strong>風格:</strong> ${style}
        </div>
        <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem;">
            點擊「開始生成」創建 4 張變體圖像
        </div>
    `;
}

// ==================== 生成圖像 ====================

async function generateImages() {
    if (!currentPromptData) {
        alert('請先與 AI 對話並完成 Prompt 設定');
        return;
    }
    
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="loading"></span> 生成中...';
    
    try {
        // 發送生成請求
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                prompt: currentPromptData.prompt,
                negative_prompt: currentPromptData.negative_prompt || '',
                num_images: 4,
                aspect_ratio: '16:9'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        const generationId = data.generation_id;
        
        addSystemMessage('🎨 圖像生成中，請稍候...');
        
        // 輪詢生成狀態
        pollGenerationStatus(generationId);
        
    } catch (error) {
        console.error('生成失敗:', error);
        addSystemMessage(`❌ 生成失敗: ${error.message}`);
        generateBtn.disabled = false;
        generateBtn.textContent = '開始生成';
    }
}

async function pollGenerationStatus(generationId) {
    const maxAttempts = 60; // 最多等待 2 分鐘
    let attempts = 0;
    
    const interval = setInterval(async () => {
        attempts++;
        
        try {
            const response = await fetch(`${API_BASE}/api/generation/${generationId}`);
            const data = await response.json();
            
            if (data.status === 'completed') {
                clearInterval(interval);
                displayGeneratedImages(data.images);
                addSystemMessage('✅ 圖像生成完成！');
                
                const generateBtn = document.getElementById('generateBtn');
                generateBtn.disabled = false;
                generateBtn.textContent = '重新生成';
                
            } else if (data.status === 'failed') {
                clearInterval(interval);
                addSystemMessage(`❌ 生成失敗: ${data.error}`);
                
                const generateBtn = document.getElementById('generateBtn');
                generateBtn.disabled = false;
                generateBtn.textContent = '重試';
            }
            
            // 超時
            if (attempts >= maxAttempts) {
                clearInterval(interval);
                addSystemMessage('⏱️ 生成超時，請重試');
                
                const generateBtn = document.getElementById('generateBtn');
                generateBtn.disabled = false;
                generateBtn.textContent = '重試';
            }
            
        } catch (error) {
            console.error('輪詢錯誤:', error);
        }
        
    }, 2000); // 每 2 秒檢查一次
}

function displayGeneratedImages(imageUrls) {
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '';
    gallery.style.display = 'grid';
    
    imageUrls.forEach((url, index) => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Generated ${index + 1}`;
        img.onclick = () => window.open(url, '_blank');
        
        item.appendChild(img);
        gallery.appendChild(item);
    });
}

// ==================== WebSocket (可選) ====================

function initWebSocket() {
    const wsUrl = `ws://localhost:8000/ws/chat/${sessionId}`;
    
    try {
        ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            console.log('WebSocket 已連線');
            updateStatus('即時連線已啟用', 'success');
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            addMessage('assistant', data.response, data.prompt_ready);
            
            if (data.prompt_ready && data.prompt_data) {
                currentPromptData = data.prompt_data;
                updatePromptPreview(data.prompt_data);
                document.getElementById('generateBtn').disabled = false;
            }
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket 錯誤:', error);
        };
        
        ws.onclose = () => {
            console.log('WebSocket 已斷線');
            updateStatus('即時連線已斷開', 'warning');
        };
        
    } catch (error) {
        console.error('WebSocket 初始化失敗:', error);
    }
}

// ==================== 工具函數 ====================

function formatTimestamp(date) {
    return new Date(date).toLocaleTimeString('zh-TW', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

console.log('✅ Gemini 前端應用已載入');
