# 台股資料查詢系統 (Taiwan Stock Market Inquiry System)

> **計算機概論與程式設計 期末專案 (Introduction to Computer Science and Programming - Final Project)**

這是以 Python 開發的桌面端應用程式。透過 Tkinter 打造圖形化介面，結合 FinMind API 獲取台股每日的交易資料，並將一年以上的歷史數據快取至 MongoDB 資料庫中，提升查詢效率、減少重複的 API 請求。也有整合維基百科，讓查詢者可以對該支股票有初步認知。

## 主要功能

* **圖形化使用者介面 (GUI)**：使用 Tkinter 實作，模仿小型應用程式，提供代號與日期輸入欄位，以及即時的執行日誌顯示。
* **動態資料獲取**：串接 [FinMind API](https://finmindtrade.com/)，自動下載從 2020 年至今的台股每日開盤、收盤、最高、最低價與成交量。
* **資料庫快取機制**：整合 MongoDB (Atlas)，將下載的股票數據持久化儲存。若資料庫已有該檔股票紀錄，則直接從資料庫讀取，大幅提升查詢速度。
* **多執行緒處理 (Threading)**：將耗時的網路請求與資料庫讀寫獨立於背景執行，確保查詢過程中主視窗不會凍結 (UI Freezing)。
* **公司背景知識庫**：整合 Wikipedia API，自動抓取並顯示查詢目標公司的維基百科摘要。

## 使用到的技術

* **前端介面**: Python Tkinter (`tkinter`, `ttk`)
* **資料處理**: Pandas
* **資料庫**: MongoDB (`pymongo`)
* **外部 API**: FinMind (`FinMind`), Wikipedia (`wikipedia`)
* **非同步處理**: `threading`

## 安裝與執行

### 1. 複製專案
```bash
git clone https://github.com/li-yeh/cs-programming-final-project.git
cd cs-programming-final-project
```
### 2. 安裝依賴套件
```bash
pip install pandas pymongo FinMind wikipedia python-dotenv
```
### 3. 設定資料庫連線
```bash
# 請將第99行換為您自己的 MongoDB 連線字串，也請記得將自己當前的IP放進IP Access List
uri = mongodb+srv://<你的帳號>:<你的密碼>@<你的叢集位址>/
```
### 4. 執行程式
```bash
python FILE_NAME.py
```
# 實作心得
整個專案本身主要是用於練習 API 的運用，我個人實作的重點主要放在資料庫的連線建立和整體運作設計上，例如 : "決定是否引用快取的判斷標準 (資料筆數) 要設在多少才是最有效益的?" 、 "資料的處理格式要怎麼切" 以及 "應用介面要如何應對使用者的錯誤輸入" ...等等，至於圖形化介面的部分，在經過幾次嘗試後，我感受到前端介面的設計需要的不只是對版面配置的美感，同時也要對整個頁面架構 (分層以及內距外距等) 有足夠熟練的運用，這對我來說是具有相當程度的上手難度，因此我選擇藉助 LLM (Gemini)的幫助，讓它先針對 tkinter 的結構做介紹，並幫我生成一個版面的模板，再做局部的修改，這大幅縮短了製作圖形介面的耗時，此外 LLM 也在處理報錯、學習新引入函式上給了我極大的幫助，這同時也考驗、增強了我資訊驗證和判讀的能力，綜上使我對專案的建置有了更多的經驗與了解。
