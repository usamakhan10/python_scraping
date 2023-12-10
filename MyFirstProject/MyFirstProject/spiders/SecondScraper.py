import scrapy
from MyFirstProject.items import MyfirstprojectItem


class SecondscraperSpider(scrapy.Spider):
    name = "SecondScraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books=response.css("article.product_pod")
        for book in books:
            relative_url = book.css("div.image_container a::attr(href)").get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url

            yield scrapy.Request(url=book_url, callback=self.individual_book_scraping)
             
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/"+next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)


    def individual_book_scraping(self, response):
        book = response.css("div.product_main")[0]
        table_rows = response.css("table tr")
        item_obj = MyfirstprojectItem()
        
        item_obj['url'] = response.url
        item_obj['title'] = book.css("h1 ::text").get()
        item_obj['upc'] = table_rows[0].css("td ::text").get()
        item_obj['product_type'] = table_rows[1].css("td ::text").get()
        item_obj['price_excl_tax'] = table_rows[2].css("td ::text").get()
        item_obj['price_incl_tax'] = table_rows[3].css("td ::text").get()
        item_obj['tax'] = table_rows[4].css("td ::text").get()
        item_obj['availability'] = table_rows[5].css("td ::text").get()
        item_obj['num_reviews'] = table_rows[6].css("td ::text").get()
        item_obj['stars'] = book.css("p.star-rating").attrib['class']
        item_obj['category'] = book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        item_obj['description'] = book.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        item_obj['price'] = book.css('p.price_color ::text').get()

        yield item_obj

