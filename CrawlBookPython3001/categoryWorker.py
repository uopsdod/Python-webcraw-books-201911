#!/usr/bin/env python3

import json
import io
import math

def execute_category():
    with io.open('../result.jl', 'r', encoding='utf-8-sig') as f:
        # ...
        dict = {};  # put it up here to record all data
        count = 0;
        for line in f:
            line = line.encode('utf-8-sig')[3:].decode('utf-8-sig')  # this works too
            # line = line.encode('utf-8')[3:].decode('utf-8')  # this works too
            jsonObj = json.loads(line)
            print(jsonObj['category'])

            # skip inaccessible information
            if 'LOGIN_REQUIRED' == jsonObj['category']:
                continue;

            # increment category count
            count += 1
            currKey = None
            for category in jsonObj['category'].split(">"):

                # construct the key for dictionary
                if currKey is None:
                    currKey = category
                else:
                    currKey = currKey + "/" + category
                # increment the value for each key
                if currKey in dict:
                    dict[currKey] += 1;
                else:
                    dict[currKey] = 1;  # initialize it as 1
                # print(category)

            # check result
            print(dict)
            print("category count {:d} ".format(count))

def execute_discount():
    # get n% book according to the discount percentage
    with io.open('result.jl', 'r', encoding='utf-8-sig') as f:
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
        books_filtered = listTopNthBooks(books, relative_nth=50) # relative_nth range from 0 ~ 100
        print("booksFiltered count: from {:d} -> {:d}".format(len(books), len(books_filtered)))
        # show result
        print(books_filtered)

def listTopNthBooks(list, relative_nth):
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
    # execute_category()
    execute_discount()
