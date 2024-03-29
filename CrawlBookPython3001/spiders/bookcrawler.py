import scrapy
from scrapy.selector import Selector
import os

class QuotesSpider(scrapy.Spider):
    '''requests are scheduled and processed asynchronously.'''
    name = 'books'
    start_urls = [
        'https://www.books.com.tw/web/sys_tdrntb/books/'
    ]

    def parse(self, response):

        bookcount = 0
        for top_selector in response.xpath(
                '//body'
                '//div[@class="mod type02_m035 clearfix"]'
                '//li[contains(@class,"item")]'
                '//div[@class="type02_bd-a"]'
        ):
            bookname_sellist = Selector(text=top_selector.get()).xpath(
                '//a[contains(@href,"loc")]'
                '//text()'
            )
            bookauthor_sellist = Selector(text=top_selector.get()).xpath(
                '//a[contains(@href,"author")]'
                '//text()'
            )
            discount_p_sellist = Selector(text=top_selector.get()).xpath(
                '//ul[@class="msg"]'
                '//li[@class="price_a"]'
                '//strong[2]'
                '//b//text()'
            )

            # if there is no discount but only price
            if len(discount_p_sellist) == 0:
                discount_p_sellist = Selector(text=top_selector.get()).xpath(
                    '//ul[@class="msg"]'
                    '//li[@class="price_a"]'
                    '//strong[1]'
                    '//b//text()'
                )

            # get bookname, bookauthor, discount_price on the 1st-layer page
            book = Book()
            if len(bookname_sellist) != 0:
                book.bookname = bookname_sellist[0].extract()
            if len(bookauthor_sellist) != 0:
                book.author = bookauthor_sellist[0].extract()
            if len(discount_p_sellist) != 0:
                book.discount_price = discount_p_sellist[0].extract()

            # go to the 2nd-layer page to get category and original_price
            inner_url = Selector(text=top_selector.get()).xpath(
                '//a/@href'
            )[0].extract()
            # must add yield to make new reuqest calls
            inner_url_request = response.follow(
                inner_url, callback=self.parse_inner_url
            )
            # meta is a field in Request to let you pass data down the river
            inner_url_request.meta['data'] = book
            yield inner_url_request

            # increment bookcount to track the total number of books we crawl
            bookcount += 1

        # verify the final book list
        print("bookcount - {:d}".format(bookcount))

    def parse_inner_url(self, response):
        # get the data passed from the previous request
        book = response.meta['data']

        # category
        category = ''
        breadcrumb_selectorlist = response.xpath(
            '//body'
            '//ul[@class="container_24 type04_breadcrumb"]'
            '//li[contains(@itemtype,"Breadcrumb")]'
            '//a//span'
            '//text()'
        )
        if len(breadcrumb_selectorlist) != 0:
            for breadcrumb_selector in breadcrumb_selectorlist:
                category += breadcrumb_selector.extract() + ">"
            category = category[:-1]  # remove the last character
            book.category = category
        else:
            book.category = 'LOGIN_REQUIRED'

        # original_price
        original_price_selectorlist = response.xpath(
            '//body'
            '//div//div//div//div'
            '//div[@class="cnt_prod002 clearfix"]'
            '//div//div'
            '//ul[@class="price"]'
            '//li//em'
            '//text()'
        )
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
        self.discount_price = ''
        self.category = ''
        self.original_price = ''


def printObject(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)


if __name__ == "__main__":
    os.system("scrapy crawl books -o ../output/bookcrawler_result.jl")
