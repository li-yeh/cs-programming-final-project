import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from pymongo import MongoClient
import datetime
from FinMind.data import DataLoader
import threading
import wikipedia

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股票資料查詢系統")
        self.root.geometry("800x700")
        self.root.iconbitmap('saber.ico')
        
        input_frame = tk.LabelFrame(root, text="查詢條件", padx=10, pady=10, font=("微軟正黑體", 12, "bold"))
        input_frame.pack(padx=10, pady=5, fill="x")
        tk.Label(input_frame, text="股票代號:", font=("微軟正黑體", 11)).grid(row=0, column=0, sticky="e")
        self.entry_stock = tk.Entry(input_frame, width=15)
        self.entry_stock.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="日期 (YYYY/MM/DD):", font=("微軟正黑體", 11)).grid(row=1, column=0, sticky="e")
        
        date_frame = tk.Frame(input_frame)
        date_frame.grid(row=1, column=1, sticky="w")
        
        self.entry_year = tk.Entry(date_frame, width=6)
        self.entry_year.pack(side="left", padx=2)
        self.entry_year.insert(0, datetime.datetime.now().year) # 預設今年

        tk.Label(date_frame, text="/", font=("微軟正黑體", 11)).pack(side="left")
        
        self.entry_month = tk.Entry(date_frame, width=4)
        self.entry_month.pack(side="left", padx=2)
        
        tk.Label(date_frame, text="/", font=("微軟正黑體", 11)).pack(side="left")
        
        self.entry_day = tk.Entry(date_frame, width=4)
        self.entry_day.pack(side="left", padx=2)

        self.btn_search = tk.Button(input_frame, text="查詢 / 下載", command=self.start_query_thread, bg="#7386FF", font=("微軟正黑體", 12, "bold"))
        self.btn_search.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")

        output_frame = tk.LabelFrame(root, text="執行結果與數據", padx=10, pady=10, font=("微軟正黑體", 12, "bold"))
        output_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.text_area = scrolledtext.ScrolledText(output_frame, height=15, font=("Consolas", 12))
        self.text_area.pack(fill="both", expand=True)

    def get_wiki_info(self, stock_id):
        try:
            self.log("正在查詢股票名稱...")
            api = DataLoader()
            df = api.taiwan_stock_info()
            row = df[df['stock_id'] == stock_id]
            
            if not row.empty:
                stock_name = row.iloc[0]['stock_name']
                wikipedia.set_lang("zh")
                summary = wikipedia.summary(stock_name, sentences=3)
                return f"【{stock_name}】維基百科簡介：\n{summary}\n" + "-"*30
            else:
                return "查無此代號對應的中文名稱，跳過維基百科。"
        except Exception as e:
            return f"維基百科查詢發生錯誤 (可能是名稱太模糊): {str(e)}"
    def log(self, message):
        
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def start_query_thread(self):

        stock_num = self.entry_stock.get().strip()
        y = self.entry_year.get().strip()
        m = self.entry_month.get().strip()
        d = self.entry_day.get().strip()

        if not stock_num or not y or not m or not d:
            messagebox.showwarning("輸入錯誤", "請填寫所有欄位")
            return

        try:
            y, m, d = int(y), int(m), int(d)
        except ValueError:
            messagebox.showerror("格式錯誤", "日期必須是數字")
            return

        self.btn_search.config(state="disabled", text="處理中...")
        self.text_area.delete(1.0, tk.END) 
        
        thread = threading.Thread(target=self.run_logic, args=(stock_num, y, m, d))
        thread.daemon = True
        thread.start()

    def run_logic(self, stocknum, y, m, d):

        wiki_result = self.get_wiki_info(stocknum)
        uri = 'mongodb+srv://yeh20060909_db_user:D0yWlZThGDsuCVdO@stockmarketinquiry.9zyiu3o.mongodb.net/'
        
        try:
            self.log('')
            self.log(f"正在連線至資料庫...")
            client = MongoClient(uri)
            db = client['stock_query']
            collection = db['stockdatas']
            
            exist_count = collection.count_documents({'symbol': stocknum}, limit=1)
            
            if exist_count <= 250:
                self.log(f"資料庫 {stocknum} 資料不足，開始從 FinMind 下載...")
                
                api = DataLoader()
                today_str = datetime.datetime.now().strftime("%Y-%m-%d")
                
                df = api.taiwan_stock_daily(
                    stock_id=stocknum,
                    start_date="2020-01-01",
                    end_date=today_str
                )

                if df.empty:
                    self.log("FinMind 未回傳任何資料，請確認股票代號。")
                    self.reset_button()
                    return

                data_dict = df.to_dict(orient='records')
                cleaned_data = []

                for row in data_dict:
                    dt_object = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
                    new_row = {
                        "timestamp": dt_object, 
                        "symbol": row['stock_id'], 
                        "open": row['open'],
                        "max": row['max'],
                        "min": row['min'],
                        "close": row['close'],
                        "volume": row['Trading_Volume'] 
                    }
                    cleaned_data.append(new_row)

                if cleaned_data:

                    collection.delete_many({'symbol': stocknum})
                    collection.insert_many(cleaned_data)
                    self.log(f"成功下載並存入 {len(cleaned_data)} 筆資料到 MongoDB")
                else:
                    self.log("處理後無有效資料可存入。")
            else:
                self.log(f"資料庫已有 {stocknum} 資料，直接查詢...")

            total_count = collection.count_documents({})
            self.log(f"目前資料庫中的總資料筆數: {total_count}")

            target_date = datetime.datetime(y, m, d, 0, 0)
            self.log(f"正在查詢日期: {target_date}...")
            
            documents = list(collection.find({'timestamp': target_date, 'symbol': stocknum}))

            if len(documents) == 0:
                self.log("------------------------")
                self.log("查無該日期的交易資料 (可能是假日或休市)。")
            else:
                self.log("------------------------")
                self.log(f"查詢結果 ({len(documents)} 筆):")
                for doc in documents:
                    result_str = (
                        f"股票: {doc.get('symbol')}\n"
                        f"日期: {doc.get('timestamp')}\n"
                        f"開盤: {doc.get('open')}\n"
                        f"最高: {doc.get('max')}\n"
                        f"最低: {doc.get('min')}\n"
                        f"收盤: {doc.get('close')}\n"
                        f"量能: {doc.get('volume')}\n"
                    )
                    self.log(result_str)
                    self.log(wiki_result)
        except Exception as e:
            self.log(f"發生錯誤: {str(e)}")
        finally:
            client.close()
            self.reset_button()

    def reset_button(self):
        self.btn_search.config(state="normal", text="查詢 / 下載")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()