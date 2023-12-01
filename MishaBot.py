#import parser
import requests
from bs4 import BeautifulSoup

import sqlite3

import telebot
from telebot import types

connect = sqlite3.connect('parser.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("DROP TABLE IF EXISTS Knife")
connect.commit()
cursor.execute('''CREATE TABLE Knife(id INTEGER PRIMARY KEY, heading TEXT, author TEXT, title TEXT, link TEXT)''')

url = "https://knife.media/"
r = requests.get(url)
soup = BeautifulSoup(r.text,'lxml')

head_article = soup.find('div', class_='widget-single__inner')
heading = head_article.find('a', class_='head').text
title = head_article.find('a', class_='widget-single__content-title').text
author = head_article.find('a', class_='meta__item').text
link = head_article.find('a', class_='widget-single__content-title').get('href')

i = 1
cursor.execute("INSERT INTO knife (id, heading, author, title, link) VALUES (?, ?, ?, ?, ?)", (i, heading, author, title, link)) #n
i += 1

articles = soup.findAll('div', class_='unit__inner')
for article in articles:
    heading = article.find('a', class_='head').text
    title = article.find('a', class_='unit__content-link').text
    author = article.find('a', class_='meta__item').text
    link = article.find('a', class_='unit__content-link').get('href')
    
    cursor.execute("INSERT INTO knife (id, heading, author, title, link) VALUES (?, ?, ?, ?, ?)", (i, heading, author, title, link))
    i += 1

connect.commit()

botTimeWeb = telebot.TeleBot('6488621618:AAGQ-RpZoUhnYEo9u0mMKqaWByGXqDHS2y8')

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

connect.close()
