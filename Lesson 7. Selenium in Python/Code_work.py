# Импорт необходимых библиотек
from selenium import webdriver
# from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import csv
import time


#  Установка веб-драйвера
driver = webdriver.Chrome()
options = Options()


# Переход на веб-сайт DomclickS
driver.get("https://ibkmiass.ru/")
result = driver.execute_script("return document.title")

search_button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/form/div[2]/div[2]').click()
apartment_block = []
ua = UserAgent()

headers = {"User-Agents": ua.random}

endpoint_2 = 'https://ibkmiass.ru/flats'

respons = requests.get(endpoint_2, headers=headers)

soup_2 = BeautifulSoup(respons.content, 'html.parser')

result = soup_2.find_all('div',('clas', "Room_room__INJTv"))




for i in result:       
    number_of_rooms = i.find('div',('class',"Room_room_descr__H5Tmv")).text
    price = i.find('div', ('class', "Room_room_total_price__6IRmI")).text
    adress = i.find('span', ('class', "Room_street__4yD91")).text
    block_= {
      'description' : number_of_rooms,
      'price' : price,
      'adress' : adress    
    }
    apartment_block.append(block_)

print(apartment_block)
    

more_btn = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/button')
    
    
time.sleep(1)

driver.quit()
      
with open('Seleniun_in_Python.csv', 'w', encoding='UTF-8') as file:
    csv_file = csv.DictWriter(file,  fieldnames=['description', 'price', 'adress'])
    csv_file.writeheader()
    csv_file.writerows(apartment_block)
  