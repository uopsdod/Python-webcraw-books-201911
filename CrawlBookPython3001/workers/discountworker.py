#!/usr/bin/env python3

import json
import io
import math


class Discountworker:
    """A class to process discount-related information"""
    def execute_discount(self, source_file_path, relative_nth):
        # get n% book according to the discount percentage
        output_path = 'CrawlBookPython3001/output/discountworker_result.txt'
        encoding_str = 'utf-8-sig'
        with io.open(source_file_path, 'r', encoding=encoding_str) as f, \
                io.open(output_path, 'w', encoding=encoding_str) as fw:
            dict = {}  # put it up here to record all data
            count = 0
            books = list()
            for line in f:
                line = line.encode(encoding_str)[3:].decode(encoding_str)
                bookJsonObj = json.loads(line)

                if 'LOGIN_REQUIRED' == bookJsonObj['original_price']:
                    continue

                oprice = float(bookJsonObj['original_price'])
                dprice = float(bookJsonObj['discount_price'])
                bookJsonObj['discount_percentage'] = (oprice - dprice) / oprice
                books.append(bookJsonObj)

            # sort the books according to the discount in a descending order
            sortk = 'discount_percentage'
            books = sorted(books, key=lambda i: i[sortk], reverse=True)
            # filter the n% books out
            # relative_nth range from 0 ~ 100
            books_filtered = self.listTopNthBooks(books,
                                                  relative_nth=relative_nth)
            # show result
            print(books_filtered)
            # store the output in dictionary format
            for book in books_filtered:
                fw.write(str(book))
                fw.write("\r\n")

    def listTopNthBooks(self, list, relative_nth):
        if relative_nth < 0:
            print("negative value for relative_nth is not allowed")
            return list[0:0]
        # floor the nth number to get top n percentage elementnt
        nth = math.floor(len(list) * (relative_nth / 100))
        return list[0:nth]


def print_object(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)

if __name__ == "__main__":
    Discountworker().execute_discount()
