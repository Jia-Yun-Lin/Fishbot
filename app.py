# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 03:40:25 2024

@author: lins8
"""

from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage)
from linebot.v3.webhooks import (MessageEvent, TextMessageContent)

app = Flask(__name__)

configuration = Configuration(access_token='NKKEbDSH6nKKcNQZ6TgvH9DyLxrxWtVxHuM4bk/m1kOoigjVUpKZztb3MBgGqyzj2T291Bro4oRXoHWc9Ukn0Y8DGRjHpnh16KvRhBqAJDXT1JZg8nrUogW5raWErF76vuDn5d4+MagVZEdBfa1bMQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7f7958a6b5ee374567f284e2360a75d9')


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()