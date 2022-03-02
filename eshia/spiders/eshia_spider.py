from urllib import response
import scrapy
import csv

# Create eshia object that inherit from scrapy.Spider to crawl
class EshiaSpider(scrapy.Spider):
    name = "eshia"

    # Set some custome settings to bypass any existing firewalls
    custom_settings = {
            # Set delay in each request to 2 second to prevent blocking from firewall
            "DOWNLOAD_DELAY" : 2,
    }

    # Create data list in initialize step to store information crawled
    def __init__(self):
        self.data = []

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
        cats_links = response.css("div#navigationBar > div:nth-child(1) > table > tr > td > ul > li > span > a::attr(href)").getall()[1:-2]
        for cat_link in cats_links:
            yield scrapy.Request(url=cat_link, callback=self.ParseSubCats)
    
    # Parsing subcategories if exist
    def ParseSubCats(self, response):
        sub_cats_links =  response.css("#navigationBar > div:nth-child(2) > table > tr > td > ul > li > span > a::attr(href)").getall()[0:-2]
        # If subcategories exist parse the content in the next function
        if sub_cats_links:
            for sub_cat_link in sub_cats_links:
                yield scrapy.Request(url=sub_cat_link, callback=self.ParseData)
        # If subcategories does not exist get contents of page
        else:
            yield scrapy.Request(url=response, callback=self.ParseData)
            
    def ParseData(self, response):
        url = response.url
        category = url.split("/")[3]
        if len(url.split("/")) == 5:
            sub_category = url.split("/")[4]
        else:
            sub_category = "None"
        
        content_table = response.css("#BooksList > tbody > tr").getall()
        for i in range(0, len(content_table)):
            content = {}
            content["Category"] = category
            content["Subcategory"] = sub_category
            content["Book name"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookName-sub > a::text').get()
            content["Book url"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookName-sub > a::attr(href)').get()
            content["Author name"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookAuthor-sub > a::text').get()
            content["Author url"] = response.css(f'#BooksList > tbody > tr:nth-child({i+1}) > td.BookAuthor-sub > a::attr(href)').get()
            
            self.data.append(content)