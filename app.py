from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('1JXF/MB34yFkRZAPuoMZ4UO7SUR56SLYOZ5sprx5Z552o7YiiGBtNBeO6Ksem1PsZXVk+/443VGx0lk+emBkFSS4sGArZgY+w+ZlD5t/FcUEV6mkdKt18L8oVNvqrLATFpFDKuFX9Hk1gxuzR3/bJQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('168306650fe21f562eca90038eb0372d')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
