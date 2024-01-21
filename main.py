# %%
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw,ImageFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from tkinter.constants import CENTER
from tkinter.messagebox import *
from tkinter import Toplevel, Label, Button, OptionMenu, StringVar
import tkinter.colorchooser as cc
from tkinter import font
from tkinter import simpledialog

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
    original_label.config(text = tat.read_local_file(fileRoute)) 

    if current_value == '原文顯示':
        pass
        #output_label.config(text = tat.read_local_file(fileRoute))    
    else:
        prompt = tat.create_prompt(current_value, str(tat.read_local_file(fileRoute)))
        result = tat.text_to_chatgpt(prompt)
        output_label.config(text = result)

def get_options_from_db():
    sql = """
        SELECT DISTINCT func_
        FROM chatgpt_prompt
    """
    return ['原文顯示'] + list(bodun.pull_data_from_mysql(sql, 'openai_info')['func_'])

def save_text():
    # 選擇存檔位置
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    # 如果用戶提供了文件名，將文本寫入文件
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            # 獲取 original_label 和 output_label 的文本內容
            original_text = original_label.cget("text")
            output_text = output_label.cget("text")

            # 寫入 original_label 的文本，加上分隔線，然後寫入 output_label 的文本
            file.write("【原文】\n")
            file.write("\n")
            file.write(original_text + "\n")
            file.write("\n")
            file.write("\n")
            file.write("【產出結果】\n")
            file.write("\n")
            file.write(output_text)

# 更新下拉式選單的函數
def update_option_menu(option_menu, options, selected_option):
    menu = option_menu["menu"]
    menu.delete(0, "end")
    for option in options:
        menu.add_command(label=option, command=lambda value=option: selected_option.set(value))

def create_insert_prompt_popup():
    # 創建一個新的頂層窗口
    popup = Toplevel(window)
    popup.title("新增 Prompt")
    popup.geometry("400x150")

    # 添加標題標籤
    Label(popup, text="請輸入欲增加的功能名稱與prompt").grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=2)

    # 功能名稱輸入框及其標籤
    Label(popup, text="功能名稱").grid(row=1, column=0, sticky='w', padx=10, pady=2)
    func_name_entry = tk.Entry(popup)
    func_name_entry.grid(row=1, column=1, padx=10, pady=2, sticky='we')

    # Prompt 輸入框及其標籤
    Label(popup, text="Prompt").grid(row=2, column=0, sticky='w', padx=10, pady=2)
    prompt_entry = tk.Entry(popup)
    prompt_entry.grid(row=2, column=1, padx=10, pady=2, sticky='we')

    # 添加確定按鈕，靠右對齊
    Button(popup, text="確定", command=lambda: add_prompt(func_name_entry.get(), prompt_entry.get(), popup)).grid(row=3, column=1, sticky='e', padx=2, pady=2)

def add_prompt(func_name, prompt_text, popup):
    if func_name and prompt_text:
        # 實際的新增邏輯
        tat.insert_new_prompt(func_name, prompt_text)

    # 可選：更新下拉式選單
    new_options = get_options_from_db()
    update_option_menu(option_menu, new_options, selected_option)

    # 關閉彈出窗口
    popup.destroy()

def fetch_current_prompt(func_name):
    sql = f"""
        SELECT prompt
        FROM chatgpt_prompt
        where func_ = '{func_name}'
    """
    if func_name != '原文顯示':
        current_prompt = bodun.pull_data_from_mysql(sql, 'openai_info')['prompt'].values[0]
    else:
        current_prompt = ''
    return current_prompt

def create_update_prompt_popup():
    # 創建一個新的頂層窗口
    popup = Toplevel(window)
    popup.title("更新 Prompt")
    popup.geometry("400x200")

    # 添加標籤
    Label(popup, text="請選擇欲調整的功能名稱").grid(row=0, column=0, padx=10, pady=2)

    # 創建 StringVar 用於下拉式選單選擇項目
    selected_func = StringVar(popup)
    options = get_options_from_db()  # 獲取選項列表
    selected_func.set(options[0])  # 設置默認選項

    # 下拉式選單
    OptionMenu(popup, selected_func, *options).grid(row=0, column=1, padx=10, pady=2)

    # 創建一個 Frame 來放置當前 Prompt 的標籤
    current_prompt_frame = tk.Frame(popup)
    current_prompt_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=2)

    # 添加顯示當前 Prompt 的標籤到 Frame 中
    current_prompt_label = Label(current_prompt_frame, text=fetch_current_prompt(options[0]), wraplength=300)
    current_prompt_label.pack()

    def on_option_change(*args):
        # 更新當前 Prompt 標籤
        current_prompt_label.config(text=fetch_current_prompt(selected_func.get()))

    # 綁定選項改變事件
    selected_func.trace('w', on_option_change)

    # 添加新 Prompt 的輸入框及其標籤
    Label(popup, text="新 Prompt").grid(row=1, column=0, padx=10, pady=2)
    new_prompt_entry = tk.Entry(popup)
    new_prompt_entry.grid(row=1, column=1, padx=10, pady=2, sticky='we')

    # 添加確定按鈕，靠右對齊
    Button(popup, text="確定", command=lambda: update_prompt(selected_func.get(), new_prompt_entry.get(), popup)).grid(row=3, column=1, sticky='e', padx=2, pady=2)

def update_prompt(func_name, new_prompt, popup):
    if func_name and new_prompt:
        # 實際的更新邏輯
        tat.update_prompt(func_name, new_prompt)

    # 重新獲取選項並更新下拉式選單
    new_options = get_options_from_db()
    update_option_menu(option_menu, new_options, selected_option)

    # 關閉彈出窗口
    popup.destroy()

def create_delete_prompt_popup(options):
    # 創建一個新的頂層窗口
    popup = Toplevel(window)
    popup.title("刪除 Prompt")
    popup.geometry("300x100")

    # 添加標籤，靠左對齊
    Label(popup, text="請選擇要刪除的prompt").grid(row=0, column=0, sticky='w', padx=10, pady=2)

    # 創建 StringVar 用於下拉式選單選擇項目
    selected_func = StringVar(popup)
    selected_func.set(options[0])  # 設置默認選項

    # 下拉式選單，靠左對齊
    options = get_options_from_db()
    OptionMenu(popup, selected_func, *options).grid(row=1, column=0, sticky='w', padx=10, pady=2)

    # 添加確定按鈕，靠右對齊
    Button(popup, text="確定", command=lambda: delete_prompt(selected_func.get(), popup)).grid(row=1, column=1, sticky='e', padx=2, pady=2)

def delete_prompt(selected_func, popup):
    if selected_func:
        # 實際的刪除邏輯
        tat.delete_prompt(selected_func)

        # 重新獲取選項並更新下拉式選單
        new_options = get_options_from_db()
        update_option_menu(option_menu, new_options, selected_option)

    # 關閉彈出窗口
    popup.destroy()


# %%
window = tk.Tk()
window.title('Text Analysis')
window.geometry('1535x790+-10+0') # 修改視窗大小(寬x高); +x+y是視窗距離螢幕的距離
# window.geometry('800x600')
window.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False 
window.iconbitmap('text_analysis.ico') # 更改左上角的icon圖示
window.configure(bg = 'white') # 修改主視窗背景顏色

# 定義一個字體對象
custom_font = font.Font(family="Microsoft JhengHei", size=10)

## 設定標題
title = tk.Label(
    text="Text Analysis",
    bg = "white",
    fg = "#0E1428",
    height = 1,
    font = ("Microsoft JhengHei", 20, 'bold'))
title.pack(side="top")

############ 文本分析區塊 ############
ta_frame = tk.Frame(window, bg='lightgray', padx=5, pady=5, highlightbackground="gray", highlightthickness=1)
ta_frame.pack(padx=10, pady=0, fill='x')

'''Label區域'''
lb = tk.Label(ta_frame, text="請選取檔案",bg ="#808080",fg="white",height=1, font=custom_font)
lb.grid(row=0, column=0, sticky='w', pady=2, padx=(0, 10))
lb2 = tk.Label(ta_frame, text="請選擇功能",bg ="#808080",fg="white", height=1, font=custom_font)
lb2.grid(row=1, column=0, sticky='w', pady=2, padx=(0, 10))
'''Label區域'''
'''Entry區域'''
loadFile_en = tk.Entry(ta_frame, width=40, font=custom_font)
loadFile_en.grid(row=0, column=1, pady=2, padx=(0, 10))
'''Entry區域'''
'''Button區域'''
loadFile_btn = tk.Button(ta_frame, text="...",height=1, command=loadFile, font=custom_font)
loadFile_btn.grid(row=0, column=2, pady=2)
ta_frame.grid_columnconfigure(3, weight=1) # 空白列，用於讓按鈕靠右對齊
output_btn = tk.Button(ta_frame, text="輸出",height=1,command = action, font=custom_font)
output_btn.grid(row=1, column=4, sticky='e', pady=2, padx=(0, 10))
save_button = tk.Button(ta_frame, text="儲存", command = save_text, font=custom_font)
save_button.grid(row=1, column=5, sticky='e', pady=2, padx=(0, 10))
'''Button區域'''
'''下拉式選單區域'''
# 設定下拉式選單的選項
options = get_options_from_db()

# 創建一個Tkinter變量，用於儲存當前的選項
selected_option = tk.StringVar()
selected_option.set("請選擇功能")  # 設定默認選項

# 創建下拉式選單
option_menu = tk.OptionMenu(ta_frame, selected_option, *options)
option_menu.grid(row=1, column=1, sticky='w', pady=2)
'''下拉式選單區域'''

############ prompt 調整區塊 ############
prompt_frame = tk.Frame(window, bg='lightgray', padx=5, pady=5, highlightbackground="gray", highlightthickness=1)
prompt_frame.pack(padx=10, pady=1, fill='x')

'''Label區域'''
lb = tk.Label(prompt_frame, text="Chatgpt Prompt 管理",bg ="#808080",fg="white",height=1, font=custom_font)
lb.grid(row=0, column=0, sticky='w', pady=2, padx=(0, 10))
'''Label區域'''
'''Button區域'''
add_prompt_btn = tk.Button(prompt_frame, text="新增 Prompt", command=create_insert_prompt_popup)
add_prompt_btn.grid(row=0, column=1, sticky='w', pady=2, padx=(0, 10))
update_prompt_btn = tk.Button(prompt_frame, text="更新 Prompt", command=create_update_prompt_popup)
update_prompt_btn.grid(row=0, column=2, sticky='w', pady=2, padx=(0, 10))
delete_prompt_btn = tk.Button(prompt_frame, text="刪除 Prompt", command=lambda: create_delete_prompt_popup(options))
delete_prompt_btn.grid(row=0, column=3, sticky='w', pady=2, padx=(0, 10))
'''Button區域'''

############ 輸出原文顯示區塊 ############
original_frame = tk.Frame(window, bg='#EBF5EE', padx=5, pady=5, highlightbackground="gray", highlightthickness=1)
# 在 original_frame 的左側增加空隙
original_frame.pack(side=tk.LEFT, padx=(10, 0), pady=0, fill='both', expand=True)

'''label區域'''
original_label = tk.Label(original_frame, text="", wraplength=500, font=custom_font)
original_label.grid(row=0, column=0, sticky='w', pady=2)
'''label區域'''

############ 輸出結果區塊 ############
output_frame = tk.Frame(window, bg='#EBF5EE', padx=0, pady=5, highlightbackground="gray", highlightthickness=1)
# 在 output_frame 的右側增加空隙
output_frame.pack(side=tk.RIGHT, padx=(1, 10), pady=0, fill='both', expand=True)

'''label區域'''
output_label = tk.Label(output_frame, text="", wraplength=500, font=custom_font)
output_label.grid(row=0, column=0, sticky='w', pady=2)
'''label區域'''

## 啟動!!!!!
window.mainloop() # 在一般python xxx.py的執行方式中，呼叫mainloop()才算正式啟動，需放於整個tkinter的最後

# %%
