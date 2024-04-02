import scrapy
from scrapy.http import HtmlResponse
from pprint import pprint
from requests import Response
from items import BooksparserItem



class Book24ruSpider(scrapy.Spider):
    
    name = "knigal"
    allowed_domains = ["knigal.ru"]
    start_urls = ["https://knigal.ru/catalog/search/result.html"]
    
    def parse(self, response:HtmlResponse):
        
        next_page = response.xpath('//a[@title="Вперед"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

        links = response.xpath('//a[@class="product photo product-item-photo"]/@href').getall()
        for link in  links:
            yield response.follow(link, callback = self.books_parse)
            
    def books_parse(self, response):
        
        name = response.xpath('//h1/text()').get()
        price = float((response.xpath('//span[@id="block_price"]/text()').get()).replace('₽', ''))
        author = response.xpath('//div[6]/span[2]/text()').get()
        
        yield BooksparserItem(name=name, price=price, author=author)
     
        
        
        
        
