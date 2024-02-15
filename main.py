#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with fastapi
# It echoes any incoming text messages and does not use the polling method.

import logging
import fastapi
import uvicorn
import telebot
from ml import predict_best_answer


API_TOKEN = '6913204816:AAGj8236SRELPY-CV_0r6nLSrhxIh98WZhs'

WEBHOOK_HOST = '3fd0-46-138-102-30.ngrok-free.app'
WEBHOOK_PORT = 8000  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_BASE = "https://{}".format(WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = fastapi.FastAPI(docs=None, redoc_url=None)


@app.post(f'/{API_TOKEN}/')
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """
    Handle '/start' and '/help'
    """
    bot.reply_to(message,
                 ("Hi I'm Ragnar, king of all vikings. How can I help you?"))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    """
    Handle all other messages
    """
    prediction = predict_best_answer(message.text)
    print(prediction)
    bot.reply_to(message, prediction)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

url = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH

# Set webhook
bot.set_webhook(
    url=url,
)


uvicorn.run(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT
)
