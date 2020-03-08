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

line_bot_api = LineBotApi('{"privateKey": {"p": "w2o9NLBJN9xu6c5ueLhsPl_QKt62yv5fp6Xnnku8C-IENjR1q0pcZSjH9P9zPrviVgIJceYQUunyhL6BoG8Se7clUc2GhLjz_8sD6nn_vt0SKAWxoeiZFgnL-OyDDWYPB3QDKyDKo1x-QRPyEOU_qYzWHSUJbE_XbPNJn1wIz1s","kty": "RSA","q": "sPe782IwmDyhnGJ2LIRhbQhL1MQLLtsFPsoSnzahLfVcjz6EhbU-hk5UOHHbDoKLxwx1RhvaivyKw5TzRpJdk0grI-hlqqdBkvRKRGjJmsE-aoOhJcG1yogvfwNXaX-s8eg3V_Rwx4Y0mdHur6Ag5UrcLsYJs_DrBs6N1YWA88k","d": "K7f1AflBYZ2t8HU3-Fk7FPst5wfvAjc-8CQk956cU9RL2vboQDg-0w0Mebyqi9nRgZf2ZriCwwediKsPF7HcdRPq2cT0UzOBH_1FSa_e5cPO4nywjEl403Q9A4T_OJd4yBrq4KOaSVwyR3RSlX0MVVT97OMD8ERFniOcu3csmVJzWeB3TG7pxhHQpAoPq7Xs-5SBYQYuY3g7DTFlH1n0p0uplJues1sIRhKLUbJwM99AmS7McmE2boB7FlL4-P4MWGrxXy8xo7hGrVmzNEQRPq_XonroMv-CW6o9ese0WPwrsECrNlLUz039Dq042eGwhNF_ajYQnt9hTXmHHDTcIQ","e": "AQAB","use": "sig","kid": "8f57164d-f3d1-4a12-991d-ee4d1d81c73c","qi": "PQ6Hu7aXGr03LpkJJTizkSka_WcdpTGvvVBEhH6L7l2Xg4QJ7kSEClEZSd7XfPYkgGxHXhSxhaumxqz2lk30fytruej2K2_OIqhb7dvm9oeHAglMvaKnW-SuLIrISEBBatnkoBvLgSdT4G8ItbRggUeHlzuWMIKYpiB8Jvb0YhM","dp": "U26vlShTCnueC0ss1XQAGx1zVmpiZwb2NjDaVDaHohcsryv0tV55VmN0BAFw5e738rrJ54xPmebyuYRQ-fuSS6nlUCjM7yu8WZEHKfxOmeHvV5Eexz705XjnUm9AgN77ObZph-dnPRpHeWeXqWkHpk9QN39Rp6HrG0RAQb7csBM","alg": "RS256","dq": "ODKz0RqBbBb1C4CJHqH7fnCABFUtZ_fNtp7dQwpKLRoaBrNHyl5AOM5vGG2vru_uC4v9QgJeaHzCZFHM38BjTv5AFOscPhFXVZ-WZhsQysBLXe_nIOJfJK4Sxzb8b1hIR5oC2T-bAQGxepecQNGNIMOhIIlrU2VSfZril8gJp2E","n": "hxYlDaqJxmRFNbNKJshZ-H7pjYEM8MuPBPxeSUhYeg6f8JWCzT2Rh2WxuZMV8vgTECrGdaSgIuLez8CO8H1h-DtJL_aDqLWU6SszeiLQ-MRDLxdU0GWkFnZvLxJ_9XWZsQMBUoPJ_L86rdYR7vP58hA2e0SXJzq0vOH7HNh7_J1bIv2vUBUhGRVu3tO-iHOvh1DNqUUkqyZ1GGFkdJHA8P5v8ziboni1pbvBvByGVnFB3-wpvkAKe4_pziJ1EQUi8TVM3jfliz_D0YkKxc9tZddfH4CIWJeaGM8W9N1TluzEqzGAZCtB-HtvXUBc9WpW3nrZzpue_zh_KVBUlD4vcw"}}')
handler = WebhookHandler('2b0d771f2d92aba60cdf667a23d82f4f')


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