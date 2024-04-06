# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class UnsplashItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()