### **SOP：Slot Game 美術規格樣板 (Photoshop) 建立流程**

**目標：** 建立一個結構化、標準化的 Photoshop (`.psd`) 樣板檔案，作為所有靜態美術素材的設計與規格基準。此樣板將定義圖層組織、命名規則、尺寸邊界與語系，以利於團隊協作及後續的自動化素材導出。

---

#### **階段 1：檔案初始化與畫布設定**

1.  **建立新檔案:**
    *   **動作:** 在 Photoshop 中建立一個新的 `.psd` 檔案。
    *   **規格:**
        *   **畫布尺寸 (Canvas Size):** 設定為遊戲的目標解析度，例如 `1920x1080` 像素。這是遊戲在 16:9 螢幕上的完整畫面。
        *   **解析度 (Resolution):** `72` pixels/inch。
        *   **色彩模式 (Color Mode):** `RGB Color`, `8-bit`。

2.  **設定參考線與網格 (Guides & Grid):**
    *   **動作:** 建立全域參考線，標示出遊戲畫面的重要區域。
    *   **建議參考線:**
        *   **安全區域 (Safe Area):** 定義在不同螢幕比例下內容保證可見的範圍。
        *   **Reel 區塊:** 標示出 5x3 或其他規格的滾輪區域。
        *   **上方 UI 區:** 標示 Jackpot、Logo 等資訊的區域。
        *   **主操作區 UI:** 標示 Spin 按鈕、下注調整、餘額顯示等控制項的區域。
    *   **目的:** 確保所有 UI 元素在設計時都有一個對齊的基準。

---

#### **階段 2：建立核心圖層群組結構**

1.  **建立主群組 (Top-Level Groups):**
    *   **動作:** 在圖層面板中，建立以下 11 個主要圖層群組。這是樣板的骨架。
    *   **群組列表:**
        1.  `介面公版` (Common_Interface)
        2.  `jackpot 公版` (Common_Jackpot)
        3.  `跑馬燈` (Marquee)
        4.  `主操作區UI` (UI_MainControls)
        5.  `上方UI` (UI_Top)
        6.  `base game 背景` (BG_BaseGame)
        7.  `free game 背景` (BG_FreeGame)
        8.  `符號` (Symbols)
        9.  `角色` (Characters)
        10. `reel` (Reels)
        11. `其他` (Misc)

2.  **建立子群組 (Sub-Groups):**
    *   **動作:** 在主群組內建立更詳細的分類子群組，增加組織性。
    *   **範例:**
        *   在 `主操作區UI` 內建立 `Buttons`, `Info_Displays`, `Bet_Controls`。
        *   在 `符號` 內建立 `High_Pay`, `Low_Pay`, `Special_Symbols`。

---

#### **階段 3：定義圖層命名與元數據規範**

這是此 SOP 的核心。所有圖層都必須遵循此命名規則，以便 AI 或腳本能解析並自動處理。

1.  **命名結構:**
    `[類型]_[名稱]_[尺寸]_[語系]_[狀態]`

2.  **欄位定義:**
    *   `[類型]`: 圖層資產的類別縮寫。
        *   `BG`: 背景 (Background)
        *   `SYM`: 符號 (Symbol)
        *   `BTN`: 按鈕 (Button)
        *   `ICON`: 圖標 (Icon)
        *   `FRAME`: 框體 (Frame)
        *   `TXT`: 文字 (Text) - *若文字內容需本地化*
        *   `IMG`: 裝飾性圖片 (Image)
        *   **`BG9`**: 可九宮格縮放的背景 (9-Slice Background)
        *   **`BTN9`**: 可九宮格縮放的按鈕 (9-Slice Button)
        *   **`FRAME9`**: 可九宮格縮放的框體 (9-Slice Frame)
        *   **`PANEL9`**: 可九宮格縮放的面板 (9-Slice Panel)
    *   `[名稱]`: 資產的具體英文或拼音名稱。
        *   `Spin`, `Wild`, `Anubis`, `JackpotTitle`
    *   `[尺寸]`: 該圖層內容的導出邊界，格式為 `寬x高` (e.g., `256x256`)。
        *   **此為硬性規定**，圖層的實際內容不得超出此邊界。建議使用圖層遮色片 (Layer Mask) 或向量形狀來限制範圍。
    *   `[語系]`: 定義此素材的語言屬性。
        *   `ALL`: 適用於所有語系 (如符號、無文字的按鈕)。
        *   `EN`: 英文。
        *   `TC`: 繁體中文。
        *   `SC`: 簡體中文。
        *   (可根據專案需求擴展其他語系代碼)
    *   `[狀態]`: (可選) 主要用於 UI 元素，定義其互動狀態。
        *   `Normal` (預設)
        *   `Hover` (滑鼠懸停)
        *   `Pressed` (點擊)
        *   `Disabled` (禁用)

3.  **命名範例:**
    *   Spin 按鈕的正常狀態: `BTN_Spin_300x150_ALL_Normal`
    *   一個可縮放的按鈕面板: `PANEL9_Default_128x128_ALL_Normal`
    *   Wild 符號: `SYM_Wild_256x256_ALL`
    *   需要翻譯的「贏得」文字標題: `TXT_WinTitle_400x100_TC`

---

#### **階段 4：建立佔位符與內容**

1.  **建立佔位符圖層:**
    *   **動作:** 根據遊戲規格文件，在對應的群組內為**每一個**所需的美術資源建立一個圖層，並使用色塊或簡單形狀作為佔位符。
    *   **關鍵:** 嚴格按照階段 3 的規範為每一個佔位符圖層命名。此時，`.psd` 檔案本身就是一份視覺化的規格與待辦清單。

2.  **轉換為智慧型物件 (Smart Objects):**
    *   **動作:** 將每一個佔位符圖層轉換為「智慧型物件」。
    *   **目的:**
        *   **非破壞性編輯:** 可以在不影響主文件佈局的情況下，獨立編輯每個素材。
        *   **易於替換:** 未來 AI 生成或人工繪製的素材，可以直接更新智慧型物件的內容，尺寸和位置會自動對應。

3.  **定義九宮格 (9-Slice) 邊界:**
    *   **對象:** 所有 `[類型]` 結尾為 `9` 的圖層 (如 `BTN9`, `PANEL9`)。
    *   **動作:** 使用 Photoshop 的 **參考線 (Guides)** 來定義九宮格的切割線。
    *   **執行步驟:**
        1.  選中目標圖層（例如 `PANEL9_Default_128x128_ALL_Normal`）。
        2.  從尺標拖曳出 **兩條垂直參考線** 和 **兩條水平參考線**。
        3.  將這四條參考線放置在圖層內容上，用以框選出中間可拉伸的區域。四個角落的內容將保持原始尺寸，不會被拉伸變形。

---

#### **階段 5：維護與導出**

1.  **版本控制:**
    *   **建議:** 使用 Git LFS (Large File Storage) 或其他雲端同步工具對此核心 `.psd` 樣板進行版本控制，方便追蹤修改歷史。

2.  **素材導出:**
    *   **方法:** 可利用 Photoshop 的「產生 -> 影像資產」功能，或搭配第三方腳本 (如 Adobe UXP Script)。
    *   **自動化基礎:** 由於圖層已包含完整的命名元數據，可以輕易編寫腳本來讀取所有圖層，並根據其名稱自動導出為對應的檔名 (e.g., `BTN_Spin_Normal.png`) 和尺寸，存放到正確的資料夾。

---

#### **階段 6：導出圖層元數據供引擎使用 (Exporting Layer Metadata for Engine)**

**目的：** 自動化產出一份結構化的數據文件（建議為 JSON 格式），該文件包含每個美術資源在遊戲引擎中佈局、渲染所需的所有參數。這將取代傳統的人工標註，大幅減少前端開發人員手動對位和設定參數的時間與錯誤率。

1.  **執行方式：Photoshop 腳本**
    *   **動作：** 此流程需要透過 Photoshop 腳本（建議使用 UXP - User Experience Platform 或舊版的 ExtendScript）來執行。腳本將遍歷 `.psd` 樣板中的所有圖層，讀取其屬性，並導出為 `layout.json` 文件。
    *   **觸發時機：** 當美術佈局完成或有任何重大更新時，由美術或技術美術 (TA) 執行此腳本。

2.  **腳本需提取的數據邏輯：**
    *   **遍歷圖層 (Iterate Layers):** 腳本會從上到下掃描所有可見圖層和群組。
    *   **解析圖層名稱 (Parse Layer Name):** 從 `[類型]_[名稱]_[尺寸]_[語系]_[狀態]` 的命名中提取元數據。
    *   **讀取圖層屬性 (Read Layer Properties):**
        *   **邊界範圍 (Bounding Box):** 讀取 `layer.bounds` 屬性，得到 `[x1, y1, x2, y2]`。
        *   **透明度 (Opacity):** 讀取 `layer.opacity` (0-100)。
        *   **混合模式 (Blend Mode):** 讀取 `layer.blendMode` (e.g., `NORMAL`, `ADD`, `MULTIPLY`)。
    *   **計算引擎用數據 (Calculate Engine Data):**
        *   **引擎內座標 (Engine Coordinates):** 腳本需要一個轉換邏輯，將 Photoshop 的左上角座標 `(x, y)` 轉換為引擎所需的座標。
        *   **Z-Index (z-index):** 腳本透過圖層的堆疊順序來生成。
        *   **九宮格邊界 (9-Slice Margins):** 當圖層類型為 `BG9`, `BTN9` 等時，腳本需偵測與圖層相交的參考線，並計算出 `left`, `top`, `right`, `bottom` 四個方向的邊界值。

3.  **產出 JSON 結構範例 (`layout.json`):**
    *   腳本最終會生成一個如下結構的 JSON 檔案。前端工程師可以直接讀取此檔案來動態生成遊戲場景。

    ```json
    {
      "scene_dimensions": {
        "width": 1920,
        "height": 1080
      },
      "assets": {
        "PANEL9_Default_Normal": {
          "source_image": "PANEL9_Default_128x128_ALL_Normal.png",
          "size": { "width": 128, "height": 128 },
          "bounds_in_canvas": { "x": 100, "y": 200, "width": 128, "height": 128 },
          "engine_coords": { "x": 164, "y": 264 },
          "pivot": { "x": 0.5, "y": 0.5 },
          "z_index": 50,
          "opacity": 100,
          "blend_mode": "NORMAL",
          "language": "ALL",
          "nine_slice_margins": {
            "left": 20,
            "top": 20,
            "right": 20,
            "bottom": 20
          }
        },
        "SYM_Wild_ALL": {
          "source_image": "SYM_Wild_256x256_ALL.png",
          "size": { "width": 256, "height": 256 },
          "bounds_in_canvas": { "x": 500, "y": 412, "width": 256, "height": 256 },
          "engine_coords": { "x": 628, "y": 540 },
          "pivot": { "x": 0.5, "y": 0.5 },
          "z_index": 80,
          "opacity": 100,
          "blend_mode": "NORMAL",
          "language": "ALL"
        }
      }
    }
    ```

---

#### **階段 7：Tile Map (瓦片地圖) 資產建立**

**目的：** 定義一個標準流程，用以在 Photoshop 中創建 Tile Map 所需的 Tileset (圖塊集) 美術資源，並闡明其與地圖數據的關係。

**1. 核心概念**

*   **Tileset (圖塊集):** 一張包含所有基礎繪圖單元（Tile，如草地、牆壁、地板）的圖片集合，類似於一張「圖章表」。這是 **在 Photoshop 中製作** 的主要對象。
*   **Tilemap Data (地圖數據):** 一個二維陣列（通常是 JSON 或 CSV 格式），記錄了地圖上每個座標點應該使用 Tileset 中的哪一個圖塊來繪製。這個數據 **不是在 Photoshop 中生成**，而是在專門的地圖編輯器（如 Tiled）或遊戲引擎中完成。

**2. Photoshop 中的 Tileset 建立流程**

1.  **建立 Tileset 專用檔案:**
    *   **動作:** 建立一個新的 `.psd` 檔案，專門用於存放一個主題的 Tileset (例如 `tileset_forest_128x128.psd`)。
    *   **命名:** 檔名應包含主題和圖塊尺寸，方便識別。
    *   **畫布尺寸:** 畫布尺寸應為圖塊尺寸的整數倍，例如，若圖塊為 `128x128`，畫布可以是 `1024x1024`（可容納 8x8 個圖塊）。

2.  **設定精確網格 (Grid):**
    *   **動作:** 在 Photoshop 中設定一個精確的網格 (`檢視 -> 顯示 -> 網格`)。
    *   **規格:** 進入 `偏好設定 -> 參考線、網格和切片`，將「格線間距」設定為你的圖塊尺寸（例如 `128` 像素），「子格」設為 `1`。
    *   **目的:** 確保每個圖塊都在精確的格子內繪製，無任何像素偏差。

3.  **繪製與組織圖塊:**
    *   **動作:**
        *   每個獨立的圖塊（如 `grass`, `dirt_path`, `tree_stump`）都應在**獨立的圖層**上繪製。
        *   將每個圖塊圖層對齊到網格中。
    *   **建議:** 可以建立圖層群組來管理不同類型的圖塊（如 `Ground_Tiles`, `Decoration_Tiles`）。

4.  **定義圖塊 ID (Tile ID):**
    *   **定義:** 每個圖塊在 Tileset 中的位置決定了它的 ID。ID 通常從 0 開始，由左到右、由上到下遞增。
    *   **溝通:** 美術師需與程式開發人員確認 ID 的計算方式（例如，是先行後列，還是先列後行）。
    *   **標註 (可選):** 可以在 Tileset 的 `.psd` 中建立一個額外的文字圖層，標示出每個圖塊的 ID，方便團隊溝通。此圖層在最終導出時應被隱藏。

5.  **導出 Tileset:**
    *   **動作:** 隱藏所有標註或非圖塊內容的圖層後，將畫布導出為一張單一的 `.png` 圖片 (例如 `tileset_forest.png`)。
    *   **結果:** 這張圖片就是將被載入到地圖編輯器或遊戲引擎中的 Tileset。

**3. 在主樣板中進行視覺預覽**

*   **目的:** 雖然地圖數據不在 Photoshop 中定義，但美術師仍需預覽地圖在實際遊戲畫面中的樣子。
*   **動作:**
    1.  在主規格樣板 (`.psd`) 中，建立一個名為 `[PREVIEW]_Tilemap` 的圖層群組。
    2.  美術師可以將導出的 Tileset 中的圖塊複製並在此群組中拼湊出場景，以預覽視覺效果。
    *   **重要:** 這個群組**僅供預覽**，其內容不會被腳本導出為任何數據或資產。`[PREVIEW]` 前綴是為了讓腳本自動忽略它。

**4. 對「階段 6」JSON 產出的影響**

*   Tileset 本身作為一張完整的圖片，可以像普通資產一樣被記錄在 `layout.json` 中，但它沒有複雜的座標資訊，通常作為一個整體資源被引用。

    ```json
    "TILES_Forest": {
      "source_image": "tileset_forest.png",
      "tile_size": { "width": 128, "height": 128 },
      "type": "tileset"
    }
    ```

---

#### **階段 8：遊戲內程式效果定義 (In-Engine Programmatic Effects)**

**1. 目的與原則**

*   **目的：** 針對「壓暗」或「Tint Color (純色覆蓋)」等常見視覺變化，不在 Photoshop 中導出多份圖片，而是定義效果參數，由遊戲引擎即時渲染。
*   **原則：** **「一份資源，多種呈現」**。這能極大地縮減遊戲包體大小和記憶體佔用。

**2. 定義方式：效果指令圖層 (Effect Instruction Layer)**

我們將使用一個特殊的**空圖層**作為指令載體，它的名稱本身就是一條指令，用來告訴腳本它要對哪個圖層做什麼效果。

*   **執行方式：**
    1.  找到你想要施加效果的目標圖層（例如 `BG_BaseGame`）。
    2.  在該圖層的**正上方**建立一個**新的空白圖層**。
    3.  根據以下命名規範，為這個空白圖層命名。

*   **效果圖層命名規範：**
    `[FX]_[效果類型]_[參數]`

*   **欄位定義：**
    *   `[FX]`: 固定前綴，代表這是一個「效果指令圖層」，腳本在處理時不會將其視為圖像導出。
    *   `[效果類型]`:
        *   `DARKEN`: 壓暗效果。
        *   `TINT`: 純色覆蓋效果。
    *   `[參數]`:
        *   對於 `DARKEN`：一個 `0` 到 `100` 的數字，代表黑色遮罩的**不透明度**。
        *   對於 `TINT`：一個 6 位的十六進制顏色碼 (不含 `#`)，例如 `FF0000` 代表紅色。

*   **範例：**
    *   **範例 1 (壓暗):**
        *   目標圖層: `BG_BaseGame_1920x1080_ALL`
        *   效果指令圖層名稱: `[FX]_DARKEN_70`
        *   **含義:** 當需要時，在 `BG_BaseGame` 上疊加一個 70% 不透明度的黑色遮罩。
    *   **範例 2 (Tint Color):**
        *   目標圖層: `SYM_Anubis_256x256_ALL`
        *   效果指令圖層名稱: `[FX]_TINT_FF3300`
        *   **含義:** 當需要時（例如角色受傷），將 `SYM_Anubis` 疊加一個 `FF3300` 的顏色。

**3. 對「階段 6」元數據導出的影響**

導出腳本需要更新邏輯來處理這些效果指令圖層。

*   **腳本更新邏輯：**
    1.  當腳本遍歷圖層時，如果遇到以 `[FX]` 開頭的圖層，則將其識別為效果指令。
    2.  腳本會讀取該指令圖層**正下方**的圖層作為**目標圖層**。
    3.  解析 `[FX]` 圖層的名稱，提取出 `效果類型` 和 `參數`。
    4.  在最終生成的 `layout.json` 中，找到目標圖層對應的物件，並在其中加入一個 `effects` 陣列，將解析出的效果資訊存入。

*   **更新後的 JSON 結構範例：**

    ```json
    {
      "scene_dimensions": { "...": "..." },
      "assets": {
        "BG_BaseGame": {
          "source_image": "BG_BaseGame_1920x1080_ALL.png",
          "...": "...",
          "z_index": 10,
          "effects": [
            {
              "type": "DARKEN",
              "opacity": 70,
              "trigger": "on_popup_show" 
            }
          ]
        },
        "SYM_Anubis": {
          "source_image": "SYM_Anubis_256x256_ALL.png",
          "...": "...",
          "z_index": 85,
          "effects": [
            {
              "type": "TINT",
              "color": "FF3300",
              "trigger": "on_character_hit"
            }
          ]
        }
      }
    }
    ```
    *(註：`trigger` (觸發時機) 是一個建議的擴展欄位，方便開發者理解何時使用此效果，它無法直接在圖層名中定義，但可由腳本根據規則或額外配置生成。)*

---

#### **階段 9：遊戲引擎遮罩定義 (Engine Mask Definition)**

**1. 目的與應用**

*   **目的：** 在 Photoshop 中定義一個圖形作為遮罩，讓遊戲引擎可以利用它來裁切或隱藏其他一個或多個圖層（即一個群組）的顯示範圍。
*   **應用場景：**
    *   **滾輪內容裁切 (Reel Clipping):** 確保滾動的符號只在滾輪的顯示區域內可見。
    *   **非矩形點擊區域 (Non-Rectangular Hit Area):** 為一個外形不規則的按鈕定義一個精確的點擊範圍。
    *   **特殊視覺效果 (Special VFX):** 使用遮罩來創造特殊的淡入淡出或擦除效果。

**2. 定義方式：遮罩圖層系統 (Mask Layer System)**

與程式效果類似，我們使用一個獨立的、有特殊命名的圖層來定義遮罩。這個圖層本身會被導出為一張灰階圖片。

*   **執行方式：**
    1.  確定你需要遮罩的目標對象。這個對象通常是一個**圖層群組**（例如 `Reel_1_Content_Group`）。
    2.  建立一個新的圖層。為方便管理，可將其放置在目標群組的頂部或一個統一的 `[MASKS]` 群組中。
    3.  在這個新圖層上，使用**純白色**繪製你希望**顯示**的區域，其他區域保持**透明或填充為純黑**。
    4.  根據以下規範為該圖層命名。

*   **遮罩圖層命名規範：**
    `[MASK]_[目標名稱]`

*   **欄位定義：**
    *   `[MASK]`: 固定前綴，代表這是一個「遮罩資源圖層」。
    *   `[目標名稱]`: 你希望此遮罩影響的**圖層群組名稱**或**圖層名稱**。這是實現關聯的關鍵。

*   **範例：**
    *   **範例 1 (滾輪遮罩):**
        *   目標群組: `Reel_1_Content_Group` (此群組包含所有在第一個滾輪中滾動的符號)。
        *   遮罩圖層名稱: `[MASK]_Reel_1_Content_Group`
        *   **含義:** 導出腳本會將此圖層導出為 `MASK_Reel_1_Content_Group.png`。遊戲引擎在渲染時，會使用這張圖作為 `Reel_1_Content_Group` 容器的遮罩。

**3. 對「階段 6」元數據導出的影響**

導出腳本需要識別 `[MASK]` 前綴的圖層並將其作為獨立的遮罩資源處理。

*   **腳本更新邏輯：**
    1.  當腳本遍歷圖層時，如果遇到以 `[MASK]` 開頭的圖層，則將其識別為一個獨立的遮罩資源。
    2.  腳本會將這個圖層**導出為一張灰階圖片**（例如 `MASK_Reel_1_Content_Group.png`）。
    3.  同時，在 `layout.json` 中，會為這個遮罩資源本身創建一個條目，並在其中記錄它所要影響的目標。

*   **更新後的 JSON 結構範例：**

    在 `assets` 物件中，除了有各類 UI 和符號資源外，還會增加遮罩資源的定義。

    ```json
    {
      "scene_dimensions": { "...": "..." },
      "assets": {
        "...": "...",
        "Reel_1_Content_Group_Mask": {
          "source_image": "MASK_Reel_1_Content_Group.png",
          "type": "mask",
          "applies_to": "Reel_1_Content_Group",
          "bounds_in_canvas": { "x": 200, "y": 100, "width": 200, "height": 600 },
          "z_index": 101 
        },
        "...": "..."
      }
    }
    ```
    *   **`type: "mask"`:** 清晰地標明這是一個遮罩資源。
    *   **`applies_to`:** 明確指出此遮罩要應用於哪個目標群組或圖層，開發人員可依此進行程式邏輯的綁定。

---

#### **階段 10：資產實例化與變形定義 (Asset Instancing & Transformation)**

**1. 目的與原則**

*   **目的：** 當佈局中需要一個已存在資產的鏡射版本時（例如，一個左箭頭和一個右箭頭），我們不需導出兩張圖片。只需導出其中一張，然後定義一個「實例 (Instance)」，並告知遊戲引擎對其進行鏡射渲染。
*   **原則：** **「一次繪製，多次使用」**。此方法適用於對稱性資源，可進一步節省材質貼圖的空間。

**2. 定義方式：實例指令圖層 (Instance Instruction Layer)**

此方法的核心是使用一個「佔位符圖層」來代表一個新物件，但這個新物件的「內容」將引用自一個已存在的「來源資產」，並對其施加變形。

*   **執行方式：**
    1.  確保你的「來源資產」圖層已存在且已正確命名（例如 `ICON_ArrowLeft_128x128_ALL`）。
    2.  在畫布上你希望「鏡射後資產」出現的位置，建立一個新的**佔位符圖層**（用色塊或簡單圖形即可）。
    3.  根據以下規範為這個新的「佔位符圖層」命名。

*   **實例圖層命名規範：**
    `[INST]_[新資產名稱]_[來源資產名稱]_[變形]`

*   **欄位定義：**
    *   `[INST]`: 固定前綴，代表這是一個「實例圖層」。導出腳本在處理它時，**不會導出圖片**，而只會生成數據。
    *   `[新資產名稱]`: 這個鏡射後的新資產在 `layout.json` 中的名稱，例如 `ArrowRight`。
    *   `[來源資產名稱]`: 被引用的「來源資產」圖層名稱中的 `[名稱]` 部分，例如 `ArrowLeft`。
    *   `[變形]`: 要施加的變形類型。
        *   `FLIP_H`: 水平鏡射 (Horizontal Flip)。
        *   `FLIP_V`: 垂直鏡射 (Vertical Flip)。

*   **範例：**
    *   **來源圖層名稱:** `ICON_ArrowLeft_128x128_ALL`
    *   **目標:** 建立一個參考此圖、但水平鏡射的右箭頭。
    *   **實例圖層名稱:** `[INST]_ArrowRight_ArrowLeft_FLIP_H`
    *   **含義:** 建立一個名為 `ArrowRight` 的新資產實例，它的外觀使用 `ArrowLeft` 的圖片，並對其進行水平鏡射。

**3. 對「階段 6」元數據導出的影響**

導出腳本需要新增對 `[INST]` 前綴的處理邏輯。

*   **腳本更新邏輯：**
    1.  當腳本遍歷圖層時，如果遇到以 `[INST]` 開頭的圖層，則將其識別為實例。
    2.  腳本**不會**為此圖層導出任何像素數據。
    3.  腳本會解析圖層名稱，獲取 `新資產名稱`、`來源資產名稱` 和 `變形` 類型。
    4.  在 `layout.json` 中，腳本會：
        a. 找到「來源資產」的 `source_image` 路徑。
        b. 建立一個屬於「新資產」的物件。
        c. 將來源圖片路徑賦予新資產，並添加一個 `transform` 物件來描述變形。

*   **更新後的 JSON 結構範例：**

    ```json
    {
      "scene_dimensions": { "...": "..." },
      "assets": {
        "ArrowLeft": {
          "source_image": "ICON_ArrowLeft_128x128_ALL.png",
          "size": { "width": 128, "height": 128 },
          "bounds_in_canvas": { "x": 300, "y": 800, "width": 128, "height": 128 },
          "z_index": 120,
          "transform": {
            "flip_h": false,
            "flip_v": false
          }
        },
        "ArrowRight": {
          "source_image": "ICON_ArrowLeft_128x128_ALL.png", 
          "size": { "width": 128, "height": 128 },
          "bounds_in_canvas": { "x": 1500, "y": 800, "width": 128, "height": 128 },
          "z_index": 121,
          "transform": {
            "flip_h": true,
            "flip_v": false
          }
        }
      }
    }
    ```
    *   如上所示，`ArrowRight` 複用了 `ArrowLeft` 的圖片資源，但擁有自己的畫布位置、`z_index`，以及一個 `transform` 屬性來告知引擎需要水平鏡射。

---

## **AI Agent 輔助連結前端引擎完整方案**

**目標：** 建立一個 AI Agent 系統，自動化處理美術規格到前端引擎的完整連結流程，包括資產生成、優化、部署和即時監控，大幅減少人工介入並提升開發效率。

---

### **階段 11：AI Agent 系統架構設計**

#### **1. 系統架構概述**

AI Agent 系統採用微服務架構，由多個專門的智能代理協同工作：

```
┌─────────────────────────────────────────────────────────┐
│                AI Agent 控制中心                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ 解析代理     │  │ 生成代理     │  │ 優化代理     │      │
│  │ Parser      │  │ Generator   │  │ Optimizer   │      │
│  │ Agent       │  │ Agent       │  │ Agent       │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ 驗證代理     │  │ 部署代理     │  │ 監控代理     │      │
│  │ Validator   │  │ Deployer    │  │ Monitor     │      │
│  │ Agent       │  │ Agent       │  │ Agent       │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```

#### **2. 核心代理功能定義**

**解析代理 (Parser Agent):**
- **職責：** 解析 PSD 檔案，提取圖層元數據
- **輸入：** `.psd` 檔案、命名規範配置
- **輸出：** 結構化元數據 JSON
- **AI 能力：** 圖像識別、命名規範驗證、錯誤檢測

**生成代理 (Generator Agent):**
- **職責：** 生成優化的遊戲資產和代碼
- **輸入：** 元數據 JSON、目標引擎配置
- **輸出：** 遊戲資產、引擎適配代碼
- **AI 能力：** 程式碼生成、資產優化建議、引擎適配

**優化代理 (Optimizer Agent):**
- **職責：** 優化資產性能和記憶體使用
- **輸入：** 原始資產、性能要求
- **輸出：** 優化後資產、壓縮報告
- **AI 能力：** 圖像壓縮、格式選擇、性能分析

---

### **階段 12：AI Agent 工作流程實施**

#### **1. 自動化工作流程設計**

```mermaid
graph TD
    A[PSD 檔案上傳] --> B[解析代理分析]
    B --> C{規範驗證}
    C -->|通過| D[生成代理處理]
    C -->|失敗| E[錯誤報告與建議]
    E --> F[人工修正]
    F --> B
    D --> G[優化代理處理]
    G --> H[驗證代理測試]
    H --> I{品質檢查}
    I -->|通過| J[部署代理發布]
    I -->|失敗| K[自動重試/人工介入]
    K --> G
    J --> L[監控代理追蹤]
    L --> M[完成報告]
```

#### **2. 詳細執行步驟**

**步驟 1: 智能檔案解析**
```json
{
  "parsing_config": {
    "auto_fix_naming": true,
    "detect_missing_assets": true,
    "validate_dimensions": true,
    "extract_nine_slice": true,
    "identify_effects": true,
    "multilang_detection": true
  }
}
```

**步驟 2: 自動程式碼生成**
- **引擎適配代碼生成**
- **資產載入器自動生成**
- **UI 佈局代碼自動化**
- **事件綁定自動設定**

**步驟 3: 智能資產優化**
- **自動圖像壓縮與格式選擇**
- **Sprite Atlas 自動生成**
- **記憶體使用優化**
- **載入順序優化**

---

### **階段 13：引擎整合介面設計**

#### **1. 統一 API 介面**

```typescript
interface AIAgentAPI {
  // 主要處理流程
  processArtworkPackage(psdFile: File, config: ProcessConfig): Promise<GameAssetPackage>;
  
  // 即時監控
  getProcessStatus(jobId: string): Promise<ProcessStatus>;
  
  // 資產管理
  updateAsset(assetId: string, changes: AssetChanges): Promise<UpdateResult>;
  
  // 性能分析
  analyzePerformance(packageId: string): Promise<PerformanceReport>;
}

interface GameAssetPackage {
  assets: AssetCollection;
  layoutData: LayoutJSON;
  engineCode: EngineAdapterCode;
  optimizationReport: OptimizationReport;
  deploymentInstructions: DeploymentGuide;
}
```

#### **2. 引擎適配器自動生成**

**Cocos Creator 適配器:**
```typescript
// 自動生成的 Cocos Creator 適配代碼
class AutoGeneratedGameScene extends cc.Component {
    @property(cc.Prefab)
    uiPrefabs: cc.Prefab[] = [];
    
    // AI 生成的資產載入邏輯
    async loadGameAssets() {
        const assetBundle = await cc.assetManager.loadBundle('game-assets');
        // ... 自動生成的載入代碼
    }
    
    // AI 生成的 UI 佈局邏輯
    setupUILayout() {
        // ... 基於元數據自動生成的佈局代碼
    }
}
```

**Unity 適配器:**
```csharp
// 自動生成的 Unity 適配代碼
public class AutoGeneratedGameManager : MonoBehaviour 
{
    [SerializeField] private AssetReferenceSprite[] symbols;
    [SerializeField] private AssetReferenceGameObject[] uiPrefabs;
    
    // AI 生成的資產管理系統
    private async void LoadGameAssets()
    {
        // ... 自動生成的 Addressables 載入代碼
    }
    
    // AI 生成的 UI 佈局系統
    private void SetupUILayout()
    {
        // ... 基於元數據自動生成的佈局代碼
    }
}
```

---

### **階段 14：智能監控與最佳化**

#### **1. 即時性能監控**

**監控代理功能:**
- **記憶體使用追蹤**
- **載入時間監控**
- **渲染性能分析**
- **使用者體驗指標**

```json
{
  "performance_metrics": {
    "memory_usage": {
      "texture_memory": "156MB",
      "audio_memory": "24MB",
      "total_memory": "180MB",
      "memory_efficiency": 0.87
    },
    "loading_performance": {
      "initial_load_time": "2.3s",
      "asset_streaming_time": "0.8s",
      "total_ready_time": "3.1s"
    },
    "rendering_performance": {
      "average_fps": 58,
      "frame_time_variance": 0.12,
      "draw_calls": 45
    }
  }
}
```

#### **2. 自動優化建議系統**

**AI 驅動的優化建議:**
```json
{
  "optimization_suggestions": [
    {
      "type": "texture_compression",
      "priority": "high",
      "description": "將 Wild 符號壓縮格式從 PNG 改為 ASTC，可節省 40% 記憶體",
      "estimated_saving": "15MB",
      "implementation_difficulty": "low",
      "auto_applicable": true
    },
    {
      "type": "sprite_atlas",
      "priority": "medium", 
      "description": "將小型 UI 圖標合併到單一 Atlas，減少 Draw Call",
      "estimated_performance_gain": "15%",
      "implementation_difficulty": "medium",
      "auto_applicable": true
    }
  ]
}
```

---

### **階段 15：AI Agent 實施計劃**

#### **1. 分階段實施策略**

**第一階段 (1-2個月): 基礎 AI Agent 建立**
- 實施解析代理和生成代理
- 建立基本的 PSD 解析能力
- 完成 JSON 元數據自動生成
- 建立簡單的引擎適配器

**第二階段 (2-3個月): 智能優化與驗證**
- 加入優化代理和驗證代理
- 實施自動圖像壓縮和格式選擇
- 建立品質檢查和錯誤檢測機制
- 完成多引擎支援

**第三階段 (1-2個月): 部署與監控**
- 實施部署代理和監控代理
- 建立即時性能監控系統
- 完成自動化部署流程
- 加入智能優化建議系統

#### **2. 技術實施需求**

**硬體需求:**
- **GPU 伺服器:** NVIDIA A100 或同等級 (用於 AI 圖像處理)
- **CPU 伺服器:** 32 核心以上 (用於並行處理)
- **儲存:** 10TB+ SSD (用於資產暫存和版本管理)
- **記憶體:** 256GB+ (用於大型 PSD 檔案處理)

**軟體架構:**
- **容器化部署:** Docker + Kubernetes
- **AI 框架:** PyTorch + TensorFlow
- **訊息佇列:** Redis + RabbitMQ
- **資料庫:** PostgreSQL + MongoDB
- **API 閘道:** FastAPI + NGINX

#### **3. 投資報酬率分析**

**成本節省:**
- **人力成本減少:** 70% (原需 3 人，現需 1 人監控)
- **開發時間縮短:** 60% (原需 2 週，現需 3 天)
- **錯誤率降低:** 85% (自動化驗證和標準化流程)
- **維護成本減少:** 50% (自動監控和優化)

**效益提升:**
- **產品交付速度:** 提升 300%
- **資產品質一致性:** 提升 95%
- **跨平台相容性:** 提升 90%
- **性能優化程度:** 平均提升 40%

---

### **階段 16：未來擴展與進化**

#### **1. AI Agent 進化路線圖**

**短期目標 (6個月):**
- 支援更多遊戲引擎 (Godot, Defold)
- 加入 3D 資產處理能力
- 實施 A/B 測試自動化
- 建立使用者行為分析

**中期目標 (1年):**
- 整合生成式 AI 進行美術創作輔助
- 實施跨專案資產重用建議
- 建立智能版本控制系統
- 加入自動化測試生成

**長期目標 (2年):**
- 發展自主學習和改進能力
- 建立行業標準化 AI Agent 平台
- 實施預測性維護和問題預防
- 整合元宇宙和 AR/VR 支援

#### **2. 持續改進機制**

**機器學習回饋循環:**
```json
{
  "learning_pipeline": {
    "data_collection": "用戶使用模式、性能數據、錯誤報告",
    "model_training": "定期重新訓練 AI 模型",
    "performance_evaluation": "A/B 測試新舊版本",
    "deployment_strategy": "漸進式部署與回滾機制"
  }
}
```

**社群貢獻系統:**
- 開放 AI Agent 擴展 API
- 建立社群驅動的優化規則庫
- 實施眾包品質檢查機制
- 鼓勵最佳實踐分享

---

### **結語**

此 AI Agent 輔助系統將徹底改變美術規格到前端引擎的連結流程，從傳統的手動、容易出錯的過程，轉變為智能化、自動化、高效率的現代化工作流程。透過分階段實施和持續改進，團隊將能夠：

1. **大幅提升開發效率** - 自動化 80% 以上的重複性工作
2. **確保品質一致性** - 標準化流程和自動驗證機制
3. **降低技術門檻** - 讓美術師專注創作，減少技術細節負擔
4. **提升產品競爭力** - 更快的迭代速度和更高的品質標準

這個 AI Agent 系統不僅是技術工具，更是團隊數位轉型的重要里程碑，為未來的智能化遊戲開發奠定堅實的基礎。