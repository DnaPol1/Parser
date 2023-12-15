# -*- coding: cp1251 -*-
import os
import telebot
from telebot import types
import sqlite3
from scraping import i

with sqlite3.connect('parser.db', check_same_thread = False) as con:
    cursor = con.cursor()
    token = os.environ['TbToken']
    botTimeWeb = telebot.TeleBot(token)

    @botTimeWeb.message_handler(commands=['start'])
    def startBot(message):
        botTimeWeb.send_message(message.chat.id, f"Привет, меня зовут Миша, и я просто супер! Отправь мне число от 1 до {i - 1}.")

    @botTimeWeb.message_handler(func=lambda message: True)
    def get_symbol(message):
        try:
            number = int(message.text)
            if number < 1:
                botTimeWeb.send_message(message.chat.id, 'Число должно быть больше 0.')
            else:
                if number <= i:
                    cursor.execute("SELECT link FROM Knife WHERE id=?",(number, ))
                    result = cursor.fetchall()
                    if result:
                        sent_link = result[0]
                    botTimeWeb.send_message(message.chat.id, f'Хорошего чтения - {sent_link}.')
                else:
                    botTimeWeb.send_message(message.chat.id, f'Число превышает {i}.')
        except ValueError:
            botTimeWeb.send_message(message.chat.id, 'Введите корректное число.')

botTimeWeb.infinity_polling()
con.close()