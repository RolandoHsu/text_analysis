# %%
import whisper
import os
import pandas as pd
import PyPDF2
from docx import Document
from bodun_package_file import bodun_package as bodun
import openai
# %%
def stt(file_name):
    """
    函式說明:
        將音檔傳成文字
    參數說明:
        1. file_name: 「string」，音檔檔名
    輸出:
        轉成文字的string
    """
    model = whisper.load_model("base")
    result = model.transcribe(file_name)
    
    return result['text']
# %%
def read_local_file(file_name):
    """
    函式說明:
        讀取本機檔案，並轉成string，可接受的檔案格式如下:
        1. txt
        2. excel
        3. pdf
        4. docx
        5. csv
    參數說明:
        1. file_name: 「string」，檔案名稱。
    輸出:
        依讀取的檔案不同，做不同的輸出
    """
    file_name_judgment = file_name.split('.')[1]

    if file_name_judgment == 'txt':
        data = pd.read_csv(file_name)
        return data
    
    elif file_name_judgment == 'xlsx':
        data = pd.read_excel(file_name)
        return data
    
    elif file_name_judgment == 'pdf':
        with open(file_name, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page = pdf_reader.pages[2]
            return page.extract_text() 
        
    elif file_name_judgment == 'docx':
        paragraphs_list = []
        doc = Document(file_name)
        for para in doc.paragraphs:
            paragraphs_list.append(para.text)
        return paragraphs_list  
    
    elif file_name_judgment == 'csv':
        data = pd.read_csv(file_name, encoding = 'big5')
        return data
    
    elif file_name_judgment == 'mp3':
        return stt(file_name)
    else:
        print('尚無此功能，請再確認')
    
# %%

def create_prompt(func_, text):
    """
    函式說明:
        依想使用的功能不同，輸出不同的prompt，
        基礎的prompt已放入mysql，僅需將text塞入基礎prompt即可       
    參數說明:
        1. func_: 「string」，輸入想要請chatgpt做的事情，目前可接受的範圍如下
    輸出:
        text
    
    """
    sql = f"""
    SELECT 
        prompt
    FROM chatgpt_prompt
    where
        func_ = '{func_}'
    """
    try:
        data = bodun.pull_data_from_mysql(sql, 'openai_info')
        return data['prompt'].values[0]+text
    except:
        print('尚無此功能的prompt，請將此功能的prompt加入openai_info.chatgpt_prompt')
# %% 

def text_to_chatgpt(prompt):
    """
    函式說明:
        使用openai API
    參數說明:
        1. prompt: 「string」，chatgpt prompt
    輸出:
        text
    """
    ## 取得存在mysql內的openai_api key
    sql = f"""
        SELECT value 
        FROM openai_info_apikey 
        where
            usser = '{os.getlogin()}'
            and factor = 'openai_api_key'
    """
    openai.api_key = bodun.pull_data_from_mysql(sql, 'openai_info')['value'].values[0]
    response = openai.Completion.create(
    model = 'gpt-3.5-turbo-instruct',
    prompt = prompt,
    max_tokens = 256,
    temperature = 0.5,
    )
    # 接收到回覆訊息後，移除換行符號
    reply_msg = response["choices"][0]["text"].replace('\n','')
    return reply_msg

def insert_new_prompt(func_, new_prompt):
    """
    函式說明:
        新增mysql openai_info.chatgpt_prompt內預設的prompt
    參數說明:
        1. func_: 「string」，資料表內的func_
        2. new_prompt: 「string」，新的prompt
    輸出:
        none
    """
    sql = f"""
    INSERT INTO openai_info.chatgpt_prompt (func_, prompt) VALUES ('{func_}', '{new_prompt}');
    """
    bodun.sql_exec(sql)

def update_prompt(func_, new_prompt):
    """
    函式說明:
        調整mysql openai_info.chatgpt_prompt內預設的prompt
    參數說明:
        1. func_: 「string」，資料表內的func_
        2. new_prompt: 「string」，新的prompt
    輸出:
        none
    """
    sql = f"""
    update openai_info.chatgpt_prompt
    set prompt = '{new_prompt}'
    where func_ = '{func_}'
    """
    bodun.sql_exec(sql)

def delete_prompt(func_):
    """
    函式說明:
        刪除mysql openai_info.chatgpt_prompt內預設的prompt
    參數說明:
        1. func_: 「string」，資料表內的func_
    輸出:
        none
    """
    sql = f"""

    delete from openai_info.chatgpt_prompt
    where func_ = '{func_}'

    """
    bodun.sql_exec(sql)

# %%
