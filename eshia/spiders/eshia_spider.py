from urllib.parse import unquote
import random
import scrapy
import csv

# Create eshia object that inherit from scrapy.Spider to crawl
class EshiaSpider(scrapy.Spider):
    name = "eshia"

    # Set some custome settings to bypass any existing firewalls
    custom_settings = {
            # Set delay in each request to 2 second to prevent blocking from firewall
            "DOWNLOAD_DELAY" : 0,
            "LOG_STDOUT" : True,
            "LOG_FILE" : './tmp/scrapy_output.txt',
    }

    # Create data list in initialize step to store information crawled
    def __init__(self):
        self.data = []
        self.content = {}

    # Save information in destruction to csv file
    def __del__(self):
        print("writing output in csv file ...")
        keys = self.data[0].keys()
        a_file = open("eshia.csv", "w", encoding="utf-8")
        dict_writer = csv.DictWriter(a_file, keys, extrasaction="ignore")
        dict_writer.writeheader()
        dict_writer.writerows(self.data)
        a_file.close()
    
    # Start sending request and gathering data
    def start_requests(self):
        urls = [
            "http://lib.eshia.ir/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.ParseCats)

    # Parsing categories
    def ParseCats(self, response):
        # Use some tricks to ommit last two items => list[1:-2]
        # cats_links = response.css("div#navigationBar > div:nth-child(1) > table > tr > td > ul > li > span > a::attr(href)").getall()[1:-2]
        # for testing #
        cats_links = response.css("div#navigationBar > div:nth-child(1) > table > tr > td > ul > li > span > a::attr(href)").getall()[7:8]
        for cat_link in cats_links:
            yield scrapy.Request(url=cat_link, callback=self.ParseSubCats)
    
    # Parsing subcategories if exist
    def ParseSubCats(self, response):
        sub_cats_links =  response.css("#navigationBar > div:nth-child(2) > table > tr > td > ul > li > span > a::attr(href)").getall()[0:-2]
        # If subcategories exist parse the content in the next function
        if sub_cats_links:
            for sub_cat_link in sub_cats_links:
                yield scrapy.Request(url=sub_cat_link, callback=self.ParseBooks)
        # If subcategories does not exist get contents of page
        elif not sub_cats_links:
            url = response.url
            self.ParseBooks(response)
            
    def ParseBooks(self, response):
        url = response.url
        category = url.split("/")[3]
        if len(url.split("/")) == 5:
            sub_category = url.split("/")[4]
        elif len(url.split("/")) == 4:
            sub_category = url.split("/")[3]
        
        content_table = response.css("#BooksList > tbody > tr").getall()
        for i in range(0, len(content_table)):
            # self.content = {}
            # self.content["Category"] = unquote(category).replace(",", "")
            # self.content["Subcategory"] = unquote(sub_category).replace(",", "")
            # self.content["Book id"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookName-sub > a::attr(href)').get().replace(",", "").split("/")[-1]
            # self.content["Book name"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookName-sub > a::text').get().replace(",", "")
            # self.content["Book url"] = book_url = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookName-sub > a::attr(href)').get().replace(",", "")
            # self.content["Author name"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookAuthor-sub > a::text').get().replace(",", "")
            # self.content["Author url"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookAuthor-sub > a::attr(href)').get().replace(",", "")
            # self.data.append(self.content)
            book_url = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookName-sub > a::attr(href)').get().replace(",", "")
            yield scrapy.Request(url=book_url, callback=self.ParseBook)

    def ParseBook(self, response):
        url = response.url
        if len(response.url.split("/")) == 4:
            url = response.url + "/1/1"
        elif len(response.url.split("/")) == 5:
            url = response.url + "/1"
        current_page = url.split("/")[-1]
        last_page = response.css("#contents_cover > table > tr:nth-child(2) > td > form:nth-child(1) > table > tr > td:nth-child(5) > a::attr(href)").get().split("/")[-1]
        random_pages = random.sample(range(int(current_page), int(last_page)), 5)
        for page in random_pages:
            page_url = '/'.join(url.split("/"))[0:-1] + str(page)
            yield scrapy.Request(url=page_url, callback=self.ParsePage)

    def ParsePage(self, response):
        self.content = {}
        self.content["Book id"] = response.url.split("/")[-3]
        self.content["Page content"] =  response.css("#contents_cover > table > tr:nth-child(4)").get().replace(",", " ").replace("\n", " ").replace("<br>", " ").replace("\r", " ")
        self.data.append(self.content)