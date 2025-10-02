# Slot Game 全流程 AI 協同最佳 SOP (sop_A)

版本: v1.0  
狀態: Draft → 可供後續細化/客製  
維護人: （請填寫）  
建立日期: 2025-10-02  

---
## 0. 高層目標與核心原則
1. 可擴充：支援多 Skin / 多 Reel 結構（3x5、4x5、Ways、Cluster 等）。
2. 法規合規：RTP 計算可審計、RNG 隨機性測試可還原、日誌留存。
3. AI 輔助但不喪失人工審核：數值、人設、美術關鍵風格與法規點設人工 Gate。
4. 可觀測：全程生成與計算結果具「可重播 Prompt + Seed + 版本標籤」。
5. DevOps 自動化：資產校驗、數值回歸、機率模擬、伺服器壓測全自動排程。
6. 安全與資料隔離：AI 生成中不外洩未公開機率與專案規劃。

---
## 1. 角色與 AI 代理矩陣 (RACI + AI)
| 領域 | 人類主責 | AI 代理角色 | AI 代理核心任務 | 最終人工 Gate |
|------|----------|-------------|----------------|---------------|
| 產品/策劃 | 產品經理 | AI 產品助手 | 競品整理/Feature 對照/PRD 草稿 | PRD 確認 |
| 數值設計 | 資深數學設計 | 數值模擬代理 | Reel 表建議、符號頻率、RTP 拆帳 | RTP & 波動簽核 |
| 數學驗證 | 數學/統計 | Monte Carlo 代理 | Spin 模擬/信賴區間 | 報告蓋章 |
| 客戶端 | 主程式 | UI 組件代理 | 狀態機骨架/動畫節奏草稿 | Code Review |
| 後端 | 系統架構師 | API 草稿代理 | OpenAPI 初稿/資料模型 | 架構審查 |
| 美術 | 美術總監 | 風格代理 | Moodboard/Prompt 優化/概念稿 | 風格鎖定 |
| 動畫/特效 | FX/動畫師 | 動畫節奏代理 | 分鏡/節奏表/特效層初稿 | 動畫審核 |
| 音效 | 音效設計 | 音效構圖代理 | 調性與 Loop 建議 | 聽審 |
| QA | QA Lead | 測試腳本代理 | 測試用例草稿/邊界建議 | 測試計畫鎖定 |
| DevOps | DevOps | Pipeline 代理 | CI YAML 草稿/資產驗證 | 安全審核 |
| 營運/數據 | 數據分析 | 分析報告代理 | KPI 預測模板 | 分析驗證 |
| 法規/合規 | 合規人員 | 條款比對代理 | 法規 Checklist 草稿 | 合規簽核 |

---
## 2. 階段總覽 (Stage Gates)
1. G0 立項：題材 + 目標市場 + RTP 區間
2. G1 Pre-Production：玩法核心 + 美術風格板 + Reel 草案 + API 草案
3. G2 垂直切片：基本轉輪 + 一次 Spin 流程 + 基礎特效
4. G3 Alpha：全部功能可跑，核心數值參數已定
5. G4 Beta：資產近最終、效能穩定、完整測試開始
6. G5 認證準備：法規包、RNG & 數學報告
7. Launch 上線：灰度 → 正式
8. LiveOps：活動循環、A/B、版本迭代

---
## 3. 詳細 SOP（含 AI 插入點）
(格式：目標 / 輸入 / 產出 / AI 任務 / 風險控制 / Gate 指標)

### 3.1 產品 & 策劃 (Pre-Production)
- 目標：定義玩法 Loop（Base / Feature / Bonus）、留存鉤子。
- 輸入：市場分析、目標客群、KPI 假設 (D1 Retention, ARPDAU, RTP 範圍)。
- 產出：PRD v1、玩法流程圖、遊戲狀態機、事件枚舉表。
- AI 任務：競品摘要 / PRD 草稿 / Player Journey 描述生成。
- 風險控制：AI 不引用未授權付費資料；人工審核可行性。
- Gate：事件表 ≥ 90% 定義，Bonus 條件清晰。

### 3.2 美術前期（Concept / Style）
- 目標：世界觀 + 符號層級辨識 + UI 視覺語言。
- 輸入：主題關鍵詞、品牌手冊、競品視覺。
- 產出：Moodboard、色彩板、Symbols 分類（高/中/低/特殊）、UI Wireframe。
- AI 任務：Prompt 優化、概念變體生成、相似度檢測。
- 風險控制：初步版權檢索 + 法務複核。
- Gate：符號縮放辨識 >95%；色彩對比 AA。

### 3.3 數值設計（Slot Math）
- 目標：建立 Reel Table / Paytable / RTP 組成與波動度分類。
- 輸入：目標 RTP (例 96% ±0.3%)、Bonus 頻率、時長 KPI。
- 產出：符號頻率表、賠付表、權重設定、Feature 觸發機制、RTP 分解表。
- AI 任務：候選 Reel 分佈 + Monte Carlo 模擬（≥1e7 Spins）+ 波動度報告。
- 風險控制：模擬 vs 理論 RTP 誤差 <0.15%；不外洩隨機種子策略。
- Gate：95% CI 報告完整，Hit Rate/Bonus 頻率在策劃帶。

### 3.4 數學驗證 & 法規包
- 目標：數學可審計 + 可重現。
- 輸入：最終 Reel + Paytable。
- 產出：RTP 理論推導、RNG 測試摘要、Log 欄位定義。
- AI 任務：格式排版、Outlier 分析、數式校對。
- 風險控制：AI 僅讀，不修改原始數據。
- Gate：追溯鏈 (版本→Commit→CSV Hash)。

### 3.5 後端服務 (Game Server & Infra)
- 目標：安全、擴展、稽核友善的 Spin API。
- 輸入：API 功能清單、事件枚舉、數值配置版本。
- 產出：OpenAPI、RNG 模組、交易/事件 Log Schema、風控 Hook。
- AI 任務：OpenAPI Draft、資料模型正規化建議、壓測腳本生成。
- 風險控制：SAST + Secrets Scan；金流計算人工審核。
- Gate：P95 Spin API <120ms；對賬 100% 一致。

### 3.6 客戶端（前端）
- 目標：平滑 Spin 體驗、動畫與結果同步、資產動態載入。
- 輸入：UI Wireframe、符號圖集、Spin Flow、API 介面。
- 產出：Reel 控制器、狀態機、資產載入器、事件總線。
- AI 任務：狀態機骨架、單元測試模板、動畫節奏建議。
- 風險控制：結果僅伺服器決定；資產哈希校驗。
- Gate：首包 <5MB，Reel FPS >55，伺服器同步 1000 測試無偏差。

### 3.7 美術製作管線
- 目標：高效率、可追溯、規範化資產產出。
- 輸入：核准概念、Style Guide。
- 產出：最終符號 / 背景 / UI 切片 / 特效序列 / Shader。
- AI 任務：變體生成、DPI/尺寸自動檢查、資產清單生成。
- 風險控制：亮度/閃爍檢測、命名規則一致。
- Gate：無未使用資產；重複率 <2%。

### 3.8 動畫 & 特效
- 目標：強化勝利回饋，控制 GPU 負載。
- 輸入：美術資產、Reel 事件。
- 產出：停輪特效、Scatter/Freespin 進場、Big Win 動畫。
- AI 任務：節奏表/分鏡草稿、粒子參數建議。
- 風險控制：Shader 複雜度限制；光閃頻率檢測。
- Gate：記憶體峰值 < 預算；Big Win 節奏 ≤4.5 秒。

### 3.9 音效 / 音樂
- 目標：強化節奏與情緒，不干擾語音/特效頻段。
- 輸入：節奏表、勝利層次表。
- 產出：Base Loop、Spin Start/Stop、Win Jingles、Feature Ambience。
- AI 任務：和弦進行建議、頻譜空間分析、Loop 無縫檢測。
- 風險控制：版權檢查；最終人工母帶。
- Gate：Loop 無聽感斷點，Loudness 合規。

### 3.10 QA（功能 / 自動化 / 數值 / 壓力 / 安全 / 合規）
- 功能、數值回歸（每日 1e6 Spins）、壓力測試、封包安全、法規比對。
- AI 任務：測試用例 (Gherkin) 草稿、Log 異常聚類、壓測報告摘要。
- 風險控制：Critical 報告人工複核。
- Gate：Critical 缺陷 0；核心覆蓋率 >90%；RTP 落點 OK。

### 3.11 DevOps / Pipeline
- 流程：Commit → Build → Test → 數值模擬 → 安全掃描 → Staging → E2E → Prod。
- AI 任務：CI 配置優化、日誌降噪、事故歸因摘要。
- 風險控制：雙人審核；金鑰 Vault。
- Gate：平均建置 <10 分鐘；回滾 <5 分鐘。

### 3.12 發佈前認證
- 產出：RTP 報告、RNG 測試、版本指紋、規則書、多語說明。
- AI 任務：多語翻譯與格式統一。
- Gate：文件一次通過 >95%。

### 3.13 上線 & 監控
- 監控：API 錯誤率、Latency、RTP Drift、Bonus Frequency、DAU/Retention。
- AI 任務：異常偵測、活動成效預測、玩家分群。
- Gate：重大異常偵測延遲 <5 分鐘。

### 3.14 LiveOps 迭代
- 內容：節慶 Skin、限時活動、排行榜/任務（不改 RNG RTP）。
- AI 任務：活動排程、資產再利用建議。
- Gate：活動回歸測試全通過。

---
## 4. 工件 (Artifacts) 與版本化建議
| 類別 | 檔案/格式 | 存放 | 版本策略 |
|------|-----------|------|-----------|
| PRD | docs/prd.md | Git | Tag (G0/G1) |
| 數值 | reel_table_vX.csv / paytable.json | Git + Hash | 改動觸發模擬 |
| RTP 報告 | rtp_report_vX.pdf | Artifact Repo | 附 Commit SHA |
| RNG 測試 | rng_testsuite_result.json | 存證桶 | 時間戳 + Seed |
| 資產 | assets/ | Git LFS/CDN | Hash 命名 |
| OpenAPI | openapi.yaml | Git | CI Schema 驗證 |
| 測試用例 | tests/*.spec | Git | 覆蓋率報表 |
| 部署設定 | infra/ helm/ | GitOps | Prod 審批 |
| 法規包 | compliance_bundle_vX.zip | Secure Store | MD5 + 簽章 |
| 儀表板 | dashboards/*.json | Observability Repo | 變更審核 |

---
## 5. AI 代理典型 Prompt 模板（示例）
1. 數值模擬代理：輸入 reels[]、paytable、targetRTP、simulations=1e7 → 輸出 Base/Feature RTP、Hit Rate、Variance、95% CI。
2. OpenAPI 代理：功能 (Spin/FeatureTrigger/Balance/History) + 授權 (JWT) → 產出 OpenAPI YAML。
3. 資產檢查代理：輸入 assets/ 結構與命名規則 → 輸出不合規清單。
4. 測試腳本代理：輸入事件列表 → Gherkin 測試案例。

---
## 6. 風險矩陣與緩解 (摘)
| 風險 | 描述 | 影響 | 緩解 |
|------|------|------|------|
| 數值漂移 | 調參未記錄 | RTP 偏離公告 | Git Hook + 自動報告 |
| 資產侵權 | AI 生成近似 IP | 法律風險 | 相似度掃描 + 法務審 |
| RNG 洩漏 | 客端推測模式 | 經濟損失 | 伺服器決定結果 + 混合熵 |
| Bonus 頻率偏差 | 經濟失衡 | ARPDAU 降 | 多組模擬選最優 |
| 發佈回滾慢 | 部署耦合 | 停機延長 | 藍綠/金絲雀 |
| AI 幻覺 | 錯誤法規語 | 認證失敗 | 嚴格術語表 + 人審 |
| 活動污染主數據 | 誤改 RTP | 合規風險 | 活動層只讀 RTP |

---
## 7. KPI 與監測指標
- 品質：崩潰率 <0.2%，Spin 錯誤率 <0.05%
- 數值：RTP 7 日漂移 <0.2%
- 效能：P95 API <120ms；首屏 <4s
- 自動化：數值每日模擬 100%；核心覆蓋 >85%
- 美術：AI 概念採納率 >30%
- 工程：MTTR <1 小時
- 營運：D1 留存 >35%；首週付費率達標

---
## 8. 目錄 & Pipeline 建議
```
/docs
  prd.md
  math/rtp_derivation.md
  compliance/
/src
  server/ (api, rng, feature_engine)
  client/ (states, reel, ui, assets)
  sim/ (simulation scripts)
/tests
  unit/ integration/ load/
/assets
  symbols/ ui/ fx/ audio/
/ci
  k6/ scripts/
/analytics
  dashboards/ queries/
```
CI 階段：Lint → Test → 數值模擬 → 資產驗證 → 安全掃描 → Staging → E2E → Prod。

---
## 9. AI 能力擴充 Roadmap
- Phase 1：文檔生成、數值模擬、測試腳本
- Phase 2：異常偵測（RTP/性能）、玩家分群
- Phase 3：動態 Reel 內測調參建議（不影響公告 RTP）
- Phase 4：玩家個人化 UX（教學/動畫強度）

---
## 10. 快速 Checklist（精簡版）
- PRD：玩法/事件/Bonus 定義完整
- 數值：理論 vs 模擬 RTP 誤差 <0.15%
- 美術：符號層級 & 命名規範檢查通過
- 客戶端：狀態機全覆蓋 & 伺服器一致性測試通過
- 後端：OpenAPI 穩定 + 風控 Hook 運作
- 測試：Critical 測試 0 Fail
- 合規：RNG & RTP 文件完成
- 監控：Dashboard & Alert 上線
- 發佈：回滾策略演練通過
- AI：所有代理輸出存檔（Prompt + Output + 版本鏈）

---
## 11. 首週實作建議
| 日 | 重點 |
|----|------|
| Day1 | PRD 草稿 + 競品報告 (AI 協助) |
| Day2 | 數值目標 + Reel 初稿 + OpenAPI 草稿 |
| Day3 | Monte Carlo 初模擬 + 客戶端狀態機骨架 |
| Day4 | 美術 Moodboard + 命名規範 + CI 初版 |
| Day5 | 模擬報告 v1 + Spin Loop 可視化 |
| Day6 | 風險清單 + 合規欄位設計 |
| Day7 | G1 Gate 審查 |

---
## 12. 總結
此 SOP 以「人類決策 + AI 生成 + 自動驗證」為核心，建立可審計、可重播、低風險的 Slot Game 研發流程。建議先落地：
1. 數值模擬代理
2. PRD/文檔生成
3. 測試腳本自動化
再逐步擴展至資產檢查、營運分析與異常監控。

---
## 13. 後續可追加的附錄（建議）
- 附錄 A：Reel/Paytable JSON Schema 樣例
- 附錄 B：Monte Carlo 模擬腳本模板 (Python)
- 附錄 C：OpenAPI YAML Draft
- 附錄 D：Gherkin 測試案例範本

(如需我生成以上附錄，請指定項目。)
