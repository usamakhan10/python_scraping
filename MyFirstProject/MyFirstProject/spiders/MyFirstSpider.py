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
        books=response.css("article.product_pod")
        for book in books:
            yield{
                "name" : book.css("h3 a::text").get(),
                "price" : book.css("div.product_price .price_color::text").get(),
                "availability" : book.css("div.product_price p.instock.availability")[0].xpath("string()").get()
            }