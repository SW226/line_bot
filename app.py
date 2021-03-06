from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UKvE1H+sIJMNnB6KIioq871IwLB1uplcJfhgGq6g4oRBf3In+1wGgsO3/i0MrlmWFT7n73kQveenyCG+BOWY4e07jiwL290+N4KwOGUjo3oPOXrl5GwtSNO7PFpK5/367Vq9bzStxb7b1CUowhI5fAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3adefbc7533092e48cc1493a318a221e')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()