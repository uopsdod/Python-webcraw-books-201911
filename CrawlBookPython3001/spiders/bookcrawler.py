import scrapy
from scrapy.selector import Selector
import os
"""

MUST_TO:
DONE understand the basics of Scrapy
DONE understnad the basics of xpath 
DONE get a rough information of the first page (88 books got)
DONE fix the issue of the only 88 books found 
DONE go to the second page (yield response.follow)
DONE get the category information
DONE output a rudimentary json output file 
DONE fix the chinese character issue in the output file 
DONE get the original price information and output it 
DONE clean the code a bit to comply with pep8
DONE sort and aggregate the category information 
DONE structure the data in the output file (some layers required)
DONE clean the code a bit to comply with pep8 
DONE sort books according to the discount percentage information and provide a method to the nth books 
* clean the code a bit to comply with pep8 
* comply all existing comments with Google docstring format 

OPTION: 
* python virtual environment
* python unitesting

"""
class QuotesSpider(scrapy.Spider):
    '''requests are scheduled and processed asynchronously.'''
    name = 'books'
    start_urls = [
        'https://www.books.com.tw/web/sys_tdrntb/books/'
    ]

    def parse(self, response):

        bookcount = 0;
        for general_selector in response.xpath('//body//div[@class="mod type02_m035 clearfix"]//li[contains(@class,"item")]//div[@class="type02_bd-a"]'): # use extract to get the textual data
            bookname_selectorlist = Selector(text=general_selector.get()).xpath('//a[contains(@href,"loc")]//text()') # this is how you reuse previous bigger Selector, probably because Selector needs <html><body>...</html></body> to wrap the content to work
            bookauthor_selectorlist = Selector(text=general_selector.get()).xpath('//a[contains(@href,"author")]//text()') # this is how you reuse previous bigger Selector
            book_discount_price_selectorlist = Selector(text=general_selector.get()).xpath('//ul[@class="msg"]//li[@class="price_a"]//strong[2]//b//text()') # this is how you reuse previous bigger Selector

            # get bookname, bookauthor, discount_price on the 1st-layer page
            book = Book();
            if len(bookname_selectorlist) != 0:
                book.bookname = bookname_selectorlist[0].extract();
            printObject("hey002", book.bookname)
            if len(bookauthor_selectorlist) != 0:
                book.author = bookauthor_selectorlist[0].extract();
            if len(book_discount_price_selectorlist) != 0:
                book.discount_price = book_discount_price_selectorlist[0].extract();

            # go to the 2nd-layer page to get category and original_price
            inner_url = Selector(text=general_selector.get()).xpath('//a/@href')[0].extract();
            inner_url_request = response.follow(inner_url, callback=self.parse_inner_url) # must add yield
            inner_url_request.meta['data'] = book; # meta is a special field in the Request class to let you pass data down the river
            yield inner_url_request;

            # increment bookcount to track the total number of books we crawl
            bookcount += 1;

        # verify the final book list
        print("bookcount - {:d}".format(bookcount))

        # for book in books:
        #     print("hey008")
        #     print("[{:s},{:s},{:s},{:s}]".format(book.bookname,book.author,book.discount_price, book.category))


    def parse_inner_url(self, response):
        book = response.meta['data']; # get the data passed from the previous request

        # category
        category = ''
        breadcrumb_selectorlist = response.xpath('//body//ul[@class="container_24 type04_breadcrumb"]//li[contains(@itemtype,"Breadcrumb")]//a//span//text()')
        if len(breadcrumb_selectorlist) != 0:
            for breadcrumb_selector in breadcrumb_selectorlist:
                category += breadcrumb_selector.extract() + ">"
            category = category[:-1]  # remove the last character
            book.category = category
        else:
            book.category = 'LOGIN_REQUIRED'

        # original_price
        original_price_selectorlist = response.xpath('//body//div//div//div//div//div[@class="cnt_prod002 clearfix"]//div//div//ul[@class="price"]//li//em//text()')
        if len(original_price_selectorlist) != 0:
            original_price = original_price_selectorlist[0].extract()
            book.original_price = original_price
        else:
            book.original_price = 'LOGIN_REQUIRED'

        # printObject("hey009",original_price)

        # output 
        yield {
            'book_name': book.bookname,
            'book_author': book.author,
            'category': book.category,
            'original_price': book.original_price,
            'discount_price': book.discount_price
        }

class Book:
    """ Book class represents books on Books.com """

    def __init__(self):
        """ initialize attributes """
        self.bookname = ''
        self.author = ''
        self.discount_price = '';
        self.category = '';
        self.original_price = '';

def printObject(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)


if __name__ == "__main__":
    os.system("scrapy crawl books -o ../output/bookcrawler_result.jl")