# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from CrawlBookPython3001.workers.categoryworker import Categoryworker
from CrawlBookPython3001.workers.discountworker import Discountworker
import json

class Crawlbookpython3001Pipeline(object):

    def __init__(self, bookcrawler_output_file_path):
        self.bookcrawler_output_file_path = bookcrawler_output_file_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bookcrawler_output_file_path = crawler.settings.get('BOOKCRAWLER_OUTPUT_FILE_PATH')
        )

    def open_spider(self, spider):
        print('Crawlbookpython3001Pipeline open_spider() called')
        self.file = open(self.bookcrawler_output_file_path, 'w')

    def process_item(self, item, spider):
        print('Crawlbookpython3001Pipeline process_item() called')
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        print('Crawlbookpython3001Pipeline close_spider() called')
        self.file.close()
        Categoryworker().execute_category(source_file_path = self.bookcrawler_output_file_path)
        Discountworker().execute_discount(source_file_path = self.bookcrawler_output_file_path)




