#!/usr/bin/env python3

import json
import io
import math

class Discountworker:
    """A class to process discount-related information"""
    def execute_discount(self, source_file_path):
        # get n% book according to the discount percentage
        with io.open(source_file_path, 'r', encoding='utf-8-sig') as f, io.open('CrawlBookPython3001/output/discountworker_result.txt', 'w', encoding='utf-8-sig') as fw:
            dict = {};  # put it up here to record all data
            count = 0;
            books = list()
            for line in f:
                line = line.encode('utf-8-sig')[3:].decode('utf-8-sig')  # this works too
                bookJsonObj = json.loads(line)

                if 'LOGIN_REQUIRED' == bookJsonObj['original_price']:
                    continue

                bookJsonObj['discount_percentage'] = (float(bookJsonObj['original_price']) - float(bookJsonObj['discount_price'])) / float(bookJsonObj['original_price'])
                books.append(bookJsonObj)

            # sort the books according to the discount percentage in a descending order
            books = sorted(books, key=lambda i: i['discount_percentage'], reverse=True)
            # filter the n% books out
            books_filtered = self.listTopNthBooks(books, relative_nth=48) # relative_nth range from 0 ~ 100
            print("booksFiltered count: from {:d} -> {:d}".format(len(books), len(books_filtered)))
            # show result
            print(books_filtered)
            # store the output in dictionary format
            for book in books_filtered:
                fw.write(str(book))
                fw.write("\r\n")

    def listTopNthBooks(self, list, relative_nth):
        if relative_nth < 0:
            print("negative value for relative_nth is not allowed")
            return list[0:0];
        nth = math.floor(len(list) * (relative_nth / 100)) # floor the nth number to get top n percentage elementnt
        return list[0:nth]

def printObject(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)

if __name__ == "__main__":
    Discountworker().execute_discount()
