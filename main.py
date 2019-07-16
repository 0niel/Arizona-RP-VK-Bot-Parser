import time
import requests
import os.path
import re
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import difflib
def get_html(url): #передаем URL
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    browser = webdriver.Chrome(chrome_options=chrome_options) # запускаем хром браузер с помощью драйвера селениум
   
    browser.get(url)             # открываем страницу с помощью URL

    
 

    time.sleep(7)                # ждем 7 секунд для того, чтобы страница прогрузилась 
                                 # и прошла проверка на антиддос.
    print(browser.current_url)
    
    html = browser.page_source   # получаем HTML страницы

    browser.quit()               # выключаем браузер
    return html                  # возвращем наш URL

def testFiles():

    t1 = open('old.txt').read().splitlines(1)  # преобразовываем наш текст
    t2 = open('new.txt').read().splitlines(1)  # в список
    rand = random.randint(199,88888888)        # генерируем случайное число для vkAPI
    message = ''.join(difflib.context_diff(t1, t2, n = 0))      # сравниваем наши файлы
    message = message.replace("!", "Изменения в рангах: ")
    re.sub("@@.*?@@","",message)  


    response = requests.get("https://api.vk.com/method/messages.send?message={0}&chat_id=1&random_id={1}&access_token=eb54565ac694ea1488c7ef04200a2ff18ff4973b61e111fc9245847cad7cd89be142c2d68e04027328cf5&v=5.101".format(message, rand))   

def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    tr = soup.find('tbody').find_all('tr')    # ищем нужную таблицу
    if (os.path.isfile("old.txt")):           
        my_file = open("new.txt", "w")
    else:
        my_file = open("old.txt", "w")
    for td in tr:
        a = td.find_all('td')                 # получаем список всех элементов с тэгом <td> в данном <tr>

        str_one = a[1]                        # берем имя игрока
        str_two = a[2]                        # берем ранг игрока

        str_one = str(str_one).replace("<td>", "").replace("</td>", "") ## убираем тэги
        str_two = str(str_two).replace("<td>", "").replace("</td>", "") ## из наших строк
 
        my_file.write('{0}:{1}\n'.format(str_one, str_two))             # записываем в файл в формате Nick_Name:RangNumber

    my_file.close()

    if (os.path.isfile("new.txt")):           
                                              # если существует new.txt, то
        testFiles()                           # сравниваем содержимое двух файлов
        os.remove('old.txt')                  # удаляем старый файл
        os.rename('new.txt', 'old.txt')       # записываем новый файл с содержимым рангов

    

def main():
    url = 'https://arizona-rp.com/mon/fraction/7/3' # ссылка на страницу мониторинга
    for _ in range(24):
        html = get_html(url)
        parse(html)

        time.sleep(3600)
    

if __name__ == '__main__':
    main()