import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin


class UnsplashImgSpider(CrawlSpider):
    name = "unsplash_img"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/t"]

    rules = (Rule(LinkExtractor(restrict_xpaths=('//div/h4')), callback="parse_item", follow=True),)
 
    def parse_item(self, response):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        
        loader.add_xpath('name', '//a[@itemprop="contentUrl"]/@title')
  
        loader.add_xpath('category', '//h1[@data-test="page-header-title"]/text()')
        
        
        relative_image_urls = response.xpath('//figure[@itemprop="image"]//a[@itemprop="contentUrl"]/@href').getall()
       
        absolut_image_url = [urljoin('https://www.unsplash.com', url_img) for url_img in relative_image_urls]
        
        loader.add_value('image_urls', absolut_image_url)
        loader.add_xpath('images', '//a[@title="Download this image"]/@href')
  
        
        yield loader.load_item()
       