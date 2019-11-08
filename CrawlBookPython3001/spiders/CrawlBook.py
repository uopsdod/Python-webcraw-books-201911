import scrapy
from scrapy.selector import Selector
from scrapy import Request
import urllib

class QuotesSpider(scrapy.Spider):
    '''requests are scheduled and processed asynchronously.'''
    name = 'books'
    start_urls = [
        'https://www.books.com.tw/web/sys_tdrntb/books/',
        # 'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        # 書名/作者/原價
        # yield {
        #     'result': response.xpath('//title')
        #     # 'result': response
        # }
        books = list();

        bookname_counter = 0;

        for general_selector in response.xpath('//body//div[@class="mod type02_m035 clearfix"]//li[contains(@class,"item")]//div[@class="type02_bd-a"]'): # use extract to get the textual data
            bookname_selectorlist = Selector(text=general_selector.get()).xpath('//a[contains(@href,"loc")]//text()') # this is how you reuse previous bigger Selector
            bookauthor_selectorlist = Selector(text=general_selector.get()).xpath('//a[contains(@href,"author")]//text()') # this is how you reuse previous bigger Selector
            book_discount_price_selectorlist = Selector(text=general_selector.get()).xpath('//ul[@class="msg"]//li[@class="price_a"]//strong[2]//b//text()') # this is how you reuse previous bigger Selector


            # 書名
            # print("bookname - {:s}".format(bookname_selectorlist.get()))
            print("count - {:d}".format(bookname_counter))
            book = Book();
            book.bookname = bookname_selectorlist[0].extract();
            book.author = bookauthor_selectorlist[0].extract();
            # if len(book_discount_price_selectorlist) != 0:
            book.discount_price = book_discount_price_selectorlist[0].extract();  # TODO: restore it

            # get the inner page link of a book
            inner_url = Selector(text=general_selector.get()).xpath('//a/@href')[0].extract();
            print("hey004")
            # print(type(inner_url))
            print(book.bookname)
            print(inner_url)
            inner_url_request = response.follow(inner_url, callback=self.parse_inner_url) # must add yield
            inner_url_request.meta['data'] = book; # meta is a special field in the Request class to let you pass data down the river
            yield inner_url_request;

            books.append(book);
            # books[counter] = book;
            bookname_counter += 1;

        # 分類/原價


        # verify the final book list
        print("bookname - count - {:d}".format(bookname_counter))
        print("bookauthor - count - {:d}".format(bookname_counter))
        print("book_discount_price - count - {:d}".format(bookname_counter))

        for book in books:
            print("hey008")
            print("[{:s},{:s},{:s},{:s}]".format(book.bookname,book.author,book.discount_price, book.category))

        #TODO: fix bookname only has 84 counts
        #TODO: fix bookauthor only has 83 counts
        #TODO: fix book_discount_price only has 84 counts

    def parse_inner_url(self, response):
        book = response.meta['data']; # get the data passed from the previous request

        category = ''
        for breadcrumb_selector in response.xpath('//body//ul[@class="container_24 type04_breadcrumb"]//li[contains(@itemtype,"Breadcrumb")]//a//span//text()'):
            category += breadcrumb_selector.extract() + ">"
        category = category[:-1] # remove the last character
        book.category = category
        print("hey009")
        print(type(category))
        print(category)

        yield {
            'category': book.category
        }

    def to_write(uni_str):
        return urllib.unquote(uni_str.encode('utf8')).decode('utf8')


class Book:
    """ Book class represents books on Books.com """

    def __init__(self):
        """ initialize attributes """
        self.bookname = ''
        self.author = ''
        self.discount_price = '';
        self.category = '';
