# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib

class ImagesPipeline:
    def process_item(self, item, spider):
        return item

class CustomImagesPipeline():
    
    def file_path(self, request, response=None, info=None, *, item=None):
        # print(f'{response.url= }')
        image_guid =[hashlib.sha1(request.url.encode()).hexdigest()]
        print({item['name']}+{image_guid})
        return f"{item['name']}-{image_guid}.avif"
        # return item
    
    
    
    




