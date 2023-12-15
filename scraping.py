# -*- coding: cp1251 -*-
import requests
from bs4 import BeautifulSoup
import sqlite3

with sqlite3.connect('parser.db', check_same_thread = False) as connection:
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Knife")
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
connection.close()