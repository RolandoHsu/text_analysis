# %%
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw,ImageFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from tkinter.constants import CENTER
from tkinter.messagebox import *
import tkinter.colorchooser as cc

from bodun_package_file import bodun_package as bodun
import text_analysis_tool as tat
# %%

#函式定義的部分
def loadFile():
    """
    函式說明:
        讀取檔案
    參數說明:
        None
    輸出:
        檔案完整路徑
    """
    if loadFile_en.get() is None:
        file_path = filedialog.askopenfilename(filetypes = (("all files","*.*"),
                                                            ("png files", "*.png"),
                                                            ("text files", "*.txt"),
                                                            ("excel files", "*.xlsx"),
                                                            ("csv files", "*.csv"),
                                                            ("pdf files", "*.pdf"),
                                                            ("word documents", "*.docx"),
                                                            ("MP3 audio files", "*.mp3"),
                                                            ("MP4 video files", "*.mp4")))
        loadFile_en.insert(0,file_path) 
    else:
        file_path = filedialog.askopenfilename(filetypes = (("all files","*.*"),
                                                            ("png files", "*.png"),
                                                            ("text files", "*.txt"),
                                                            ("excel files", "*.xlsx"),
                                                            ("csv files", "*.csv"),
                                                            ("pdf files", "*.pdf"),
                                                            ("word documents", "*.docx"),
                                                            ("MP3 audio files", "*.mp3"),
                                                            ("MP4 video files", "*.mp4")))
        loadFile_en.delete(0,'end')
        loadFile_en.insert(0,file_path) 

def action():
    fileRoute = loadFile_en.get()
    
    current_value = selected_option.get()
    
    if current_value == '原文顯示':
        output_label.config(text = tat.read_local_file(fileRoute))    
    else:
        prompt = tat.create_prompt(current_value, str(tat.read_local_file(fileRoute)))
        result = tat.text_to_chatgpt(prompt)
        output_label.config(text = result)

def save_text():
    # 選擇存檔位置
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    # 如果用户提供了文件名，将文本写入文件
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output_label.cget("text"))


# %%
window = tk.Tk()
window.title('Text Analysis')
window.geometry('1535x790+-10+0') # 修改視窗大小(寬x高); +x+y是視窗距離螢幕的距離
# window.geometry('380x400')
window.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False 
# window.geometry('380x400')
window.iconbitmap('text_analysis.ico') # 更改左上角的icon圖示
window.configure(bg = 'white') # 修改主視窗背景顏色

## 設定標題
title = tk.Label(
    text="Text Analysis",
    bg = "white",
    fg = "black",
    height = 1,
    font = ("Microsoft JhengHei", 20, 'bold'))
title.pack(side="top")

'''Label區域'''
lb = tk.Label(text="請選取檔案",bg ="grey",fg="white",height=1)
lb.place(x=20 ,y=40)
lb2 = tk.Label(text="請選擇功能",bg ="grey",fg="white",height=1)
lb2.place(x=20 ,y=70)
output_label = tk.Label(text="", font=("Arial", 12), wraplength=500)
output_label.place(x=20 ,y=120)
'''Label區域'''
'''Entry區域'''
loadFile_en = tk.Entry(width=40)
loadFile_en.place(x=90 ,y=40)
'''Entry區域'''
'''Button區域'''
loadFile_btn = tk.Button(text="...",height=1,command=loadFile)
loadFile_btn.place(x=375 ,y=40)
output_btn = tk.Button(text="輸出",height=1,command = action)
output_btn.place(anchor="center",x=375 ,y=90)
save_button = tk.Button(text="儲存", command = save_text)
save_button.place(anchor="center",x=420 ,y=90)
'''Button區域'''
'''下拉式選單區域'''
# 設定下拉式選單的選項
sql = f"""
    SELECT 
        DISTINCT func_
    FROM chatgpt_prompt
    """
options = ['原文顯示']+list(bodun.pull_data_from_mysql(sql, 'openai_info')['func_'])

# 創建一個Tkinter變量，用於儲存當前的選項
selected_option = tk.StringVar()
selected_option.set("請選擇功能")  # 設定默認選項

# 創建下拉式選單
option_menu = tk.OptionMenu(window, selected_option, *options)
option_menu.place(x=90 ,y=70)
'''下拉式選單區域'''

## 啟動!!!!!
window.mainloop() # 在一般python xxx.py的執行方式中，呼叫mainloop()才算正式啟動，需放於整個tkinter的最後

# %%