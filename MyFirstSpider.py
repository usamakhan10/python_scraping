import scrapy

# creating scrapy project
#prev command : scrapy startproject MyFirstProject

# creating a generic spider
#command : scrapy genspider MyFirstSpider books.toscrape.com

class MyfirstspiderSpider(scrapy.Spider):
    name = "MyFirstSpider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        pass
