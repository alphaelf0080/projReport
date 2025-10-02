### **AI 代理輔助 Slot Game 開發標準作業流程 (SOP)**

#### **階段 0：專案啟動與基礎設定**

1.  **需求定義 (人類輸入):**
    *   **您需要提供：** 遊戲主題、核心玩法（例如：滾輪數量、線數、特殊機制如 "Free Spins", "Bonus Game"）、目標玩家、美術風格方向。
    *   **AI 執行：** AI 根據您的輸入，建立一份專案規格文件 (`spec.md`)，並使用 `google_web_search` 尋找相關主題的參考資料和競品分析。

2.  **技術選型與環境建置 (AI 主導):**
    *   **AI 執行：**
        *   **前端:** 提案使用 `React` + `Pixi.js` (2D 渲染) 或 `Phaser.js`。
        *   **後端:** 提案使用 `Node.js` + `Express.js` (輕量快速) 或 `Python` + `FastAPI` (適合複雜計算)。
        *   **AI 動作:** AI 會向您確認技術選型，待您同意後，使用 `run_shell_command` 執行 `npx create-react-app` 或其他腳手架工具，建立專案基本結構、安裝 `npm` 依賴套件，並執行 `git init` 初始化版本控制。

#### **階段 1：數值設計 (Math Model)**

1.  **核心參數定義 (人類輸入):**
    *   **您需要提供：** 遊戲的目標 RTP (Return to Player，玩家回報率)、波動率 (Volatility)、最大贏錢倍數、各類符號的期望出現頻率。
    *   **AI 執行：** AI 將這些參數記錄在案。

2.  **賠率表與滾輪生成 (AI 主導):**
    *   **AI 執行：**
        *   AI 會編寫一個 Python 或 JavaScript 腳本 (`math_generator.py`)。
        *   此腳本會根據您給定的 RTP 和參數，透過演算法生成一組滾輪 strip 和符號的賠率表 (Paytable)。
        *   產出 `paytable.json` 和 `reels.json` 檔案。

3.  **模擬與驗證 (AI 自動化):**
    *   **AI 執行：**
        *   AI 編寫另一個模擬腳本 (`simulation.py`)，讀取 `reels.json`。
        *   使用 `run_shell_command` 執行此腳本，進行十億次以上的模擬旋轉。
        *   分析模擬結果，驗證實際 RTP 是否逼近目標 RTP，並產出波動率、命中率等數據的驗證報告 (`simulation_report.txt`)。
        *   **如果驗證失敗，AI 會自動調整 `math_generator.py` 的參數並重複步驟 2 和 3，直到結果符合預期。**

#### **階段 2：美術設計與資源產出 (Art Assets)**

1.  **美術風格探索 (AI 輔助):**
    *   **AI 執行：** 根據您在階段 0 提供的遊戲主題，使用 `google_web_search` 搜尋 "sci-fi slot game art", "ancient egypt game UI" 等關鍵字，提供視覺風格參考圖 (Moodboard)。

2.  **資源清單建立 (AI 自動化):**
    *   **AI 執行：** AI 掃描 `paytable.json` 和 `spec.md`，自動生成一份所需美術資源的完整清單 (`asset_list.md`)，包含：
        *   高、中、低階符號
        *   特殊符號 (Wild, Scatter, Bonus)
        *   遊戲背景
        *   UI 元素 (按鈕、邊框、提示框)
        *   動畫特效 (贏錢、滾輪轉動、特殊功能觸發)

3.  **佔位符資源生成 (AI 自動化):**
    *   **AI 執行：** 這是關鍵步驟，讓前端開發可以先行。AI 會：
        *   為每個符號和 UI 元素，使用工具或程式碼生成簡單的幾何圖形或帶有文字標示的圖片（例如：一個寫著 "WILD" 的方塊）作為**佔位符 (Placeholder)**。
        *   使用 `write_file` 將這些佔位符資源存入 `public/assets/placeholders/` 目錄。

4.  **最終美術資源整合 (人類提供，AI 整合):**
    *   **您需要提供：** 由美術設計師製作的最終 `.png`, `.jpg`, spritesheet 等檔案。
    *   **AI 執行：** AI 會將您提供的最終資源，根據 `asset_list.md` 的命名規則，覆蓋掉 `placeholders` 目錄中的佔位符檔案，完成資源替換。

#### **階段 3：前端開發 (Frontend Development)**

1.  **組件化開發 (AI 自動化):**
    *   **AI 執行：** 使用 `write_file` 創建 React 組件：
        *   `Game.js`: 遊戲主場景。
        *   `Reel.js`: 單個滾輪。
        *   `Symbol.js`: 單個符號。
        *   `UI.js`: 控制下注、旋轉的用戶介面。
        *   初始時，所有組件都會讀取並顯示**佔位符**美術資源。

2.  **遊戲邏輯與狀態管理 (AI 自動化):**
    *   **AI 執行：** 編寫前端遊戲邏輯，包括：
        *   點擊 "Spin" 按鈕的行為。
        *   管理遊戲狀態（如：`isSpinning`, `balance`, `lastWin`）。
        *   滾輪開始、加速、減速、停止的動畫邏輯。

3.  **API 串接 (AI 自動化):**
    *   **AI 執行：** 編寫 `api.js` 模組，使用 `fetch` 或 `axios` 與後端溝通。定義 `/spin` API 的請求和回應格式。當收到後端的回應後，更新 `Game.js` 的狀態以顯示結果。

#### **階段 4：後端開發 (Backend Development)**

1.  **API 端點建立 (AI 自動化):**
    *   **AI 執行：** 使用 `Express.js` 或 `FastAPI` 框架，建立核心的 `/spin` API 端點。此端點接收玩家的下注額作為參數。

2.  **核心邏輯實現 (AI 自動化):**
    *   **AI 執行：**
        *   讀取並載入階段 1 產出的 `reels.json` 數值模型。
        *   實現一個安全的隨機數生成器 (RNG)。
        *   當 `/spin` 被呼叫時，後端根據 `reels.json` 和 RNG 的結果，計算出本次旋轉的符號組合、是否有贏錢、贏錢金額、以及是否觸發特殊功能。
        *   將結果以 JSON 格式回傳給前端。

3.  **玩家狀態管理 (AI 自動化):**
    *   **AI 執行：** 實現一個簡單的玩家錢包管理機制。在原型階段，可以是一個簡單的伺服器內存對象或本地 JSON 檔案，用於追蹤玩家餘額。

#### **階段 5：品質保證與測試 (QA & Testing)**

1.  **單元測試 (Unit Testing) (AI 自動化):**
    *   **AI 執行：**
        *   **後端:** 編寫測試腳本，針對 `/spin` 端點的各種情況（如：贏錢、輸錢、觸發 Free Spin）進行測試，確保賠率計算正確。
        *   **前端:** 編寫測試來驗證 UI 組件的渲染和互動是否正常。
        *   使用 `run_shell_command` 執行 `npm test` 或 `pytest` 來運行所有測試。

2.  **整合測試 (Integration Testing) (AI 自動化):**
    *   **AI 執行：** 確保前端發送請求後，能正確接收並渲染後端回傳的遊戲結果。

3.  **端到端 (E2E) 測試與自動遊玩 (AI 自動化):**
    *   **AI 執行：**
        *   使用 `Playwright` 或 `Cypress` 等工具編寫 E2E 測試腳本。
        *   該腳本會模擬真實玩家行為：啟動遊戲 -> 調整下注 -> 連續點擊旋轉 1000 次 -> 檢查餘額變化是否合理。
        *   使用 `run_shell_command` 執行測試。

4.  **最終驗收 (人類執行):**
    *   **您需要執行：**
        *   親自遊玩遊戲，檢查美術表現、動畫流暢度、音效（如果有的話）和整體體驗。
        *   提供主觀回饋和需要調整的細節。AI 會根據您的回饋進行修改。
