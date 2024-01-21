# text_analysis
1. 針對輸入的檔案，串接chatgpt api執行文字分析，預設之chatgpt prompt儲存於mysql。
* 可接受的檔案
  * mp3、mp4 : 載入時將同步完成語音轉文字(by whisper)
  * txt、csv
  * xlsx
  * word
  * pdf
* 串接工具
  * python: 主功能、function 撰寫
  * whisper: 針對輸入的mp3、mp4等語音檔進行語音轉文字
  * chatgpt: 將預設的prompt及丟入的檔案文字串接api，執行文字翻譯、摘要...等預設功能。
  * mysql: 儲存預測之chatgpt prompt
* 目前可執行之功能
  * 翻譯
  * 摘要
  * 中翻英
  * 會議記錄
  * 情感分析
  * 關鍵字分析 

2. 針對儲存於mysql之預設chatgpt prompt，新增按鈕進行調整，功能包含:
* 新增prompt
* 更新prompt
* 刪除prompt

3. 流程圖
![圖片](https://github.com/RolandoHsu/text_analysis/blob/main/image/%E6%B5%81%E7%A8%8B%E5%9C%96.png?raw=true)

4. 介面
![圖片]()
