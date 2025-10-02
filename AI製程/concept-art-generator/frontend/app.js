/**
 * Slot Game Concept Art Generator - Frontend Logic
 */

const API_BASE = 'http://localhost:8000';

// 全域狀態
let currentBriefId = null;
let currentGenerationId = null;
let generatedImages = [];
let selectedImages = [];

// ========== 初始化 ==========
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    showStep(1);
});

function initEventListeners() {
    // Brief 表單提交
    document.getElementById('briefForm').addEventListener('submit', handleBriefSubmit);
    
    // 生成按鈕
    document.getElementById('btnGenerate').addEventListener('click', handleGenerate);
    
    // 反饋提交
    document.getElementById('btnSubmitFeedback').addEventListener('click', handleFeedbackSubmit);
    
    // 下載全部
    document.getElementById('btnDownloadAll').addEventListener('click', handleDownloadAll);
}

// ========== 步驟控制 ==========
function showStep(stepNumber) {
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
    document.getElementById(`step${stepNumber}`).classList.add('active');
}

// ========== Brief 提交 ==========
async function handleBriefSubmit(e) {
    e.preventDefault();
    
    showStatus('正在建立 Brief...', 'info');
    
    try {
        // 收集表單資料
        const formData = new FormData(e.target);
        
        // 解析關鍵詞
        const styleKeywords = formData.get('styleKeywords')
            .split(',')
            .map(k => k.trim())
            .filter(k => k);
        
        // 解析色彩
        const primaryColors = parseColors(formData.get('primaryColors'));
        const secondaryColors = parseColors(formData.get('secondaryColors'));
        
        // 解析參考圖
        const referenceUrls = formData.get('referenceUrls')
            .split('\n')
            .map(url => url.trim())
            .filter(url => url);
        
        const referenceImages = referenceUrls.map((url, idx) => ({
            id: `ref_${idx}`,
            url: url,
            tags: [],
            weight: 1.0
        }));
        
        // 組合請求
        const briefData = {
            theme: formData.get('theme'),
            styleKeywords: styleKeywords,
            colorPreferences: {
                primary: primaryColors,
                secondary: secondaryColors,
                mood: null
            },
            referenceImages: referenceImages,
            targetCount: parseInt(formData.get('targetCount')),
            targetRatio: formData.get('targetRatio'),
            constraints: {
                violence: false,
                religiousSymbols: false
            }
        };
        
        // 發送請求
        const response = await fetch(`${API_BASE}/api/brief`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(briefData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        currentBriefId = result.briefId;
        
        // 顯示摘要
        displayBriefSummary(result);
        
        showStatus('Brief 建立成功！', 'success');
        showStep(2);
        
    } catch (error) {
        console.error('建立 Brief 失敗:', error);
        showStatus(`錯誤: ${error.message}`, 'error');
    }
}

function parseColors(colorString) {
    if (!colorString) return [];
    return colorString
        .split(',')
        .map(c => c.trim())
        .filter(c => c && c.startsWith('#'));
}

function displayBriefSummary(briefData) {
    const summary = document.getElementById('briefSummary');
    
    let paletteHtml = '';
    if (briefData.extractedPalette && briefData.extractedPalette.length > 0) {
        paletteHtml = `
            <div class="palette">
                ${briefData.extractedPalette.map(color => 
                    `<div class="color-swatch" style="background-color: ${color}" title="${color}"></div>`
                ).join('')}
            </div>
        `;
    }
    
    summary.innerHTML = `
        <div class="brief-summary">
            <h3>Brief 摘要</h3>
            <p><strong>ID:</strong> ${briefData.briefId}</p>
            <p><strong>主題:</strong> ${briefData.theme}</p>
            <p><strong>風格:</strong> ${briefData.styleTokens.join(', ')}</p>
            ${paletteHtml ? `<p><strong>提取色板:</strong></p>${paletteHtml}` : ''}
            <p><strong>預估時間:</strong> 約 ${briefData.estimatedTime} 秒</p>
        </div>
    `;
}

// ========== 圖像生成 ==========
async function handleGenerate() {
    if (!currentBriefId) {
        showStatus('請先建立 Brief', 'error');
        return;
    }
    
    const btn = document.getElementById('btnGenerate');
    btn.disabled = true;
    btn.textContent = '生成中...';
    
    showProgress(0, '正在準備生成...');
    
    try {
        // 發送生成請求
        const generateData = {
            briefId: currentBriefId,
            count: 4,
            ratio: document.getElementById('targetRatio').value,
            seed: null,
            variations: null
        };
        
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(generateData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        currentGenerationId = result.generationId;
        
        // 開始輪詢進度
        pollGenerationStatus();
        
    } catch (error) {
        console.error('生成失敗:', error);
        showStatus(`錯誤: ${error.message}`, 'error');
        btn.disabled = false;
        btn.textContent = '開始生成';
        hideProgress();
    }
}

async function pollGenerationStatus() {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/api/generation/${currentGenerationId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const result = await response.json();
            
            // 更新進度
            if (result.progress !== null) {
                showProgress(result.progress, result.message || '生成中...');
            }
            
            // 檢查是否完成
            if (result.status === 'completed') {
                clearInterval(interval);
                hideProgress();
                displayGeneratedImages(result.images);
                showStatus('生成完成！', 'success');
                
                const btn = document.getElementById('btnGenerate');
                btn.disabled = false;
                btn.textContent = '重新生成';
                
                showStep(3);
            } else if (result.status === 'failed') {
                clearInterval(interval);
                hideProgress();
                showStatus(`生成失敗: ${result.message}`, 'error');
                
                const btn = document.getElementById('btnGenerate');
                btn.disabled = false;
                btn.textContent = '重試';
            }
            
        } catch (error) {
            console.error('查詢狀態失敗:', error);
            clearInterval(interval);
            hideProgress();
            showStatus(`錯誤: ${error.message}`, 'error');
        }
    }, 2000); // 每 2 秒查詢一次
}

function showProgress(percentage, text) {
    const container = document.getElementById('generationProgress');
    const bar = document.getElementById('progressBar');
    const textElem = document.getElementById('progressText');
    
    container.style.display = 'block';
    bar.style.width = `${percentage}%`;
    textElem.textContent = text;
}

function hideProgress() {
    document.getElementById('generationProgress').style.display = 'none';
}

// ========== 顯示生成圖像 ==========
function displayGeneratedImages(images) {
    generatedImages = images;
    selectedImages = [];
    
    const gallery = document.getElementById('imageGallery');
    gallery.innerHTML = '';
    
    images.forEach((img, idx) => {
        const card = document.createElement('div');
        card.className = 'image-card';
        card.dataset.imageId = img.id;
        
        card.innerHTML = `
            <img src="${API_BASE}${img.url}" alt="Generated ${idx + 1}">
            <div class="image-info">
                <div class="image-meta">
                    <span>Seed: ${img.seed}</span>
                    <span>${img.size.width}×${img.size.height}</span>
                </div>
                <div class="rating">
                    ${[1, 2, 3, 4, 5].map(star => 
                        `<span class="star" data-rating="${star}">★</span>`
                    ).join('')}
                </div>
                <input type="checkbox" class="image-select" id="select_${img.id}">
                <label for="select_${img.id}">選擇</label>
            </div>
        `;
        
        // 點選卡片選擇
        card.addEventListener('click', (e) => {
            if (e.target.classList.contains('star')) {
                handleRating(img.id, parseInt(e.target.dataset.rating));
            } else if (!e.target.classList.contains('image-select')) {
                toggleImageSelection(card, img.id);
            }
        });
        
        gallery.appendChild(card);
    });
    
    // 顯示反饋面板
    document.getElementById('feedbackPanel').style.display = 'block';
}

function toggleImageSelection(card, imageId) {
    const checkbox = card.querySelector('.image-select');
    checkbox.checked = !checkbox.checked;
    
    if (checkbox.checked) {
        card.classList.add('selected');
        if (!selectedImages.includes(imageId)) {
            selectedImages.push(imageId);
        }
    } else {
        card.classList.remove('selected');
        selectedImages = selectedImages.filter(id => id !== imageId);
    }
}

function handleRating(imageId, rating) {
    // 更新星星顯示
    const card = document.querySelector(`[data-image-id="${imageId}"]`);
    const stars = card.querySelectorAll('.star');
    
    stars.forEach((star, idx) => {
        if (idx < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
    
    // 儲存評分（暫存在記憶體）
    const img = generatedImages.find(i => i.id === imageId);
    if (img) {
        img.rating = rating;
    }
}

// ========== 反饋提交 ==========
async function handleFeedbackSubmit() {
    if (selectedImages.length === 0) {
        showStatus('請至少選擇一張圖片', 'error');
        return;
    }
    
    showStatus('正在提交反饋...', 'info');
    
    try {
        // 收集評分
        const ratings = {};
        generatedImages.forEach(img => {
            if (img.rating) {
                ratings[img.id] = img.rating;
            }
        });
        
        // 收集調整建議
        const adjustmentsText = document.getElementById('adjustments').value;
        const adjustments = adjustmentsText
            .split('\n')
            .map(a => a.trim())
            .filter(a => a);
        
        const feedbackData = {
            generationId: currentGenerationId,
            selections: selectedImages,
            ratings: ratings,
            tags: null,
            adjustments: adjustments
        };
        
        const response = await fetch(`${API_BASE}/api/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(feedbackData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        showStatus('反饋已提交，權重已更新！', 'success');
        
        // 顯示建議
        if (result.suggestedAdjustments && result.suggestedAdjustments.length > 0) {
            const suggestions = result.suggestedAdjustments.join('\n');
            alert(`系統建議:\n${suggestions}`);
        }
        
        // 返回步驟 2 重新生成
        showStep(2);
        
    } catch (error) {
        console.error('提交反饋失敗:', error);
        showStatus(`錯誤: ${error.message}`, 'error');
    }
}

// ========== 下載全部 ==========
function handleDownloadAll() {
    generatedImages.forEach((img, idx) => {
        const link = document.createElement('a');
        link.href = `${API_BASE}${img.url}`;
        link.download = `concept_art_${idx + 1}.png`;
        link.click();
    });
    
    showStatus('開始下載所有圖片...', 'success');
}

// ========== 狀態訊息 ==========
function showStatus(message, type = 'info') {
    const statusElem = document.getElementById('statusMessage');
    statusElem.textContent = message;
    statusElem.className = `status-message ${type}`;
    statusElem.style.display = 'block';
    
    setTimeout(() => {
        statusElem.style.display = 'none';
    }, 5000);
}
