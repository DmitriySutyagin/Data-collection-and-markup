from pymongo import MongoClient
import json

client = MongoClient('localhost',27017)

db = client['books']
books = db.info
path = r'D:\MyTrainig\Data_collection_and_markup\Lesson_2.json'

with open(path,'r', encoding='UTF-8') as f:
   json_file = json.load(f)

books.insert_one(json_file)

for book in books.find({'Price' : 51.77}):
   # for i in book:
      print(f'{book= }', sep='\n')
   # pass