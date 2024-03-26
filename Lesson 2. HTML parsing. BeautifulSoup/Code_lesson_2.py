import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import json
import os

name = []
price =[]
availability = []
descriptions = []
count = 0



ua = UserAgent()

headers = {"User-Agents": ua.random}

endpoint = 'http://books.toscrape.com/'

while True:

    count += 1
    print(f'Этап номер: {count}')
    

    
    respons = requests.get(endpoint, headers=headers)

    soup = BeautifulSoup(respons.content, 'html.parser')

    next_page = soup.find('li',('class', 'next'))
    result = soup.find_all('li', ('class', 'col-xs-6 col-sm-4 col-md-3 col-lg-3') )
    
    endpoint_2 = []


    for i in result:        
        for link in i.find_all('div', ('class', 'image_container')):
            endpoint_2.append(link.find('a').get('href'))

    url_joined = []
   
    for link in endpoint_2:
        if endpoint != 'http://books.toscrape.com/':
            endpoint = 'http://books.toscrape.com/catalogue/'
            url_joined.append(endpoint +link)
        else:
            endpoint = 'http://books.toscrape.com/'
            url_joined.append(endpoint + link)
        
    for i in url_joined:
  
        response = requests.get(i)
        soup_2 = BeautifulSoup(response.content, 'html.parser')

        try:
            soup_name = soup_2.find('h1').text

            name.append(soup_name)
        
        except:
            print('Отсутствует название книги')

        try:
            soup_price = soup_2.find('p', ('class', 'price_color')).text
            soup_price = float(re.sub(r'[^\d.]', '', soup_price))
            price.append(soup_price)
    
        except:
            print('Цена товара отсутствует')
        try:
            soup_availability = soup_2.find('p', ('class', 'instock availability')).text
            soup_availability = int(re.sub(r'[^\d.]', '', soup_availability))
            availability.append(soup_availability)
        except:
            print('Отсутствуют данные о наличии')

        try:
            soup_descriptions = soup_2.find_all('p')
            for i in soup_descriptions:
                if len(i.get_text(strip=True)) >30:
                    descriptions.append(i.get_text(strip=True))
        except:
            print('Описание остутствует')

    output = {'Name' : name, 'Price': price, "Availabiliry" : availability, 'Descriptions' : descriptions}



    if not next_page:
        break

    if next_page == 'catalogue/page-2.html':
        
        endpoint = 'http://books.toscrape.com/'

        endpoint = endpoint + next_page

    else:
        endpoint = 'http://books.toscrape.com/catalogue/'
        *_, suffix = next_page.find('a').get('href').split('/')
        endpoint = endpoint + suffix


with open('Lesson_2.json','w',encoding='utf-8') as f:
   json_file = json.dump(output, f, ensure_ascii=False,indent=2)