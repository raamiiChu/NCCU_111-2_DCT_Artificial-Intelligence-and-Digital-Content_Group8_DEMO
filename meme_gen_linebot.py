# 函式註解
from typing import *

from flask import Flask, request, abort

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, QuickReply, QuickReplyButton, MessageAction

# 從 ./crawler.py 載入
from crawler import MemeGeneratorPredisAI, text_preprocessing

app = Flask(__name__)
line_bot_api = LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')

def meme_generator(user_id, message_text: str) -> None:
    # 對輸入文本進行預處理，回傳 List[str]
    text = text_preprocessing([message_text])
    URL = "https://predis.ai/free-ai-tools/ai-meme-generator/#"

    # 至少 4 個詞彙才會執行
    if len(text) >= 4:
        line_bot_api.push_message(
            user_id, 
            TextSendMessage(text="製作中，大約需要 30 秒完成")
        )

        # 詞彙之間以空格做間隔
        text = " ".join(text)

        # 開始網路爬蟲
        Generator = MemeGeneratorPredisAI(URL)
        Generator.open_webdriver()
        meme_url = Generator.genrate_meme(text)
        Generator.close()

        # 有小機率會產圖失敗
        if meme_url == "https://brain.predis.ai/templates_images/644252de15522fe7315e3009_1.jpeg":
            line_bot_api.push_message(
                user_id, 
                TextSendMessage(text="製作失敗，請稍後再嘗試")
            )
        else:
            image_message = ImageSendMessage(original_content_url=meme_url, preview_image_url=meme_url)
            
            line_bot_api.push_message(
                user_id, 
                image_message
            )
    else:
        line_bot_api.push_message(
            user_id, 
            TextSendMessage(text="詞彙量過少，請輸入至少 4 個詞彙")
        )

@app.route("/webhook", methods=['POST'])
def linebot():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)

# Function to send the message with the auto-appearing button
def handle_message(event):
    user_id = event.source.user_id
    if event.message.type != "text":
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="不好意思，我無法處理文字以外的請求，請確認您輸入的是文字，謝謝~")
        )
        return
    else:
        meme_generator(user_id, event.message.text)

if __name__=="__main__":  #如果以主程式執行
    app.run() # 最後生成網址，貼到line: messaging API-->webhook url