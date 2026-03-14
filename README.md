# 📈 台灣股票資料查詢系統 (Taiwan Stock Market Inquiry System)

> **計算機概論與程式設計 期末專案 (Introduction to Computer Science and Programming - Final Project)**

這是一個使用 Python 開發的桌面端應用程式。透過 Tkinter 打造圖形化介面，結合 FinMind API 獲取台灣股市每日交易資料，並將歷史數據快取至 MongoDB 資料庫中，以提升查詢效率與減少重複的 API 請求。此外，系統亦整合了維基百科，於查詢時同步顯示該公司的基本簡介。

## ✨ 核心功能 (Features)

* **圖形化使用者介面 (GUI)**：使用 Tkinter 實作，提供直覺的股票代號與日期輸入欄位，以及即時的執行日誌顯示。
* **動態資料獲取**：串接 [FinMind API](https://finmindtrade.com/)，自動下載從 2020 年至今的台股每日開盤、收盤、最高、最低價與成交量。
* **資料庫快取機制**：整合 MongoDB (Atlas)，將下載的股票數據持久化儲存。若資料庫已有該檔股票紀錄，則直接從資料庫讀取，大幅提升查詢速度。
* **多執行緒處理 (Threading)**：將耗時的網路請求與資料庫讀寫獨立於背景執行，確保查詢過程中主視窗不會凍結 (UI Freezing)。
* **公司背景知識庫**：整合 Wikipedia API，自動抓取並顯示查詢目標公司的維基百科摘要。

## 🛠️ 系統技術棧 (Tech Stack)

* **前端介面**: Python Tkinter (`tkinter`, `ttk`)
* **資料處理**: Pandas
* **資料庫**: MongoDB (`pymongo`)
* **外部 API**: FinMind (`FinMind`), Wikipedia (`wikipedia`)
* **非同步處理**: `threading`

## 🚀 安裝與執行 (Installation & Usage)
pip install pandas pymongo FinMind wikipedia certifi
### 1. 複製專案 (Clone the repository)
```bash
git clone [https://github.com/li-yeh/cs-programming-final-project.git](https://github.com/li-yeh/cs-programming-final-project.git)
cd cs-programming-final-project
