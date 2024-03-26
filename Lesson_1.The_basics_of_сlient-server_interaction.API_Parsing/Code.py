import requests
import json

client_id = "0"
client_secret = "__"

categories = input("Укажите категорию которая вас интересует: ")
city = input("Введите название города: ")

endpoint =  "https://api.foursquare.com/v3/places/search"

params = {
    
    "client_id": client_id,
    "near" : city,
    "client_secret": client_secret,
    "query": categories,
}

headers = {
    "Accept": "application/json",
    "Authorization": client_secret
}


response = requests.get(endpoint, params=params, headers=headers)


if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]

    for venue in venues:
        try:
            print("Название:", venue["name"])
            print("Город", venue["location"]["locality"])
            print("Регион", venue["location"]["region"])
            print("Адрес:", venue["location"]["address"])
            print("\n")
        except:
            print("Нет значения")
            print('\n')
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
