import requests
from lxml import html, etree
from pymongo import MongoClient


def insert_to_db(list_movies):
    
    "This function makes a connection to the local mongodb server. Creates a database and uploads data to it"
    
    client = MongoClient('localhost', 27017)
    db = client['Job_opening']
    collection = db['Accidental_Cancellations']
    collection.insert_many(list_movies)
    client.close
    
    
headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

resp = requests.get(url='https://perm.hh.ru/search/vacancy?text=&area=1400&hhtmFrom=main&hhtmFromLabel=vacancy_search_line', 
                    headers=headers
                    )

print(resp.status_code)

tree = html.fromstring(html=resp.content)

vacancii = tree.xpath('//body//span/a[@class="bloko-link"]/@href')

list_block = []
db_parsing = []

for i in vacancii:
    list_block.append(i)
    
for link_vacan in list_block:
    
    dict_parsing = {}
    
    resp_2 = requests.get(link_vacan, headers=headers)
    
    tree_2 = html.fromstring(html=resp_2.content)

    try:        
        name = tree_2.xpath('//body//h1[@data-qa="vacancy-title"]/text()')[0]
        dict_parsing['name'] = name
    except:
        print('None name')
        
    try:
        salary = ''.join(tree_2.xpath('//body//div/span[@class="bloko-header-section-2 bloko-header-section-2_lite"]/text()'))
        dict_parsing['salary'] = salary
    except:
        print('Отустсвует значение по зарплате')
        
    try:
        experience = tree_2.xpath('//body//span[@data-qa="vacancy-experience"]/text()')[0]
        dict_parsing['experience'] = experience
    except:
        print('Значение опыта осутствует')
        
    try:
        work_schedule = ', '.join(tree_2.xpath('//body//p[2]//text()')[0:3:2])
        dict_parsing['work_schedule'] = work_schedule
    except:
        print('Отсутствуют данные о графике работы')
        
    try:
        employer = tree_2.xpath('//body//span[@data-qa="bloko-header-2"]//text()')
        employer = employer[0]
        dict_parsing['employer'] = employer
    except:
        print('Данные о работадателе отсутствуют')
        
    # try: 
    #     employers_adress = tree_2.xpath('//body//span[@data-qa="vacancy-view-raw-address"]/text()')
    #     print(employers_adress)
    # except:
    #     print('Отсутстыует данные адреса работадателя')
        
    try:
        rating = tree_2.xpath('//body//div[@class="bloko-text bloko-text_extra-large bloko-text_strong"]/text()')
        rating = rating[0]
        dict_parsing['rating'] = rating
    except:
        print('Отсутствуют данные по рейтингу работадателя')
        
    db_parsing.append(dict_parsing)
    
insert_to_db(db_parsing)