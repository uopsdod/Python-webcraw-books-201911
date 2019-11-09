#!/usr/bin/env python3

import json
import io



def printObject(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)

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
    # get n% book according to the discount
    with io.open('result.jl', 'r', encoding='utf-8-sig') as f:
        dict = {};  # put it up here to record all data
        count = 0;
        books = list()
        for line in f:
            line = line.encode('utf-8-sig')[3:].decode('utf-8-sig')  # this works too
            # line = line.encode('utf-8')[3:].decode('utf-8')  # this works too
            bookJsonObj = json.loads(line)
            printObject("hey002", bookJsonObj)

            if 'LOGIN_REQUIRED' == bookJsonObj['original_price']:
                continue

            print("{:s}-{:s}-{:f}".format(bookJsonObj['original_price'], bookJsonObj['discount_price'], float(bookJsonObj['original_price'])/float(bookJsonObj['discount_price'])));
            bookJsonObj['discount_percentage'] = (float(bookJsonObj['original_price']) - float(bookJsonObj['discount_price'])) / float(bookJsonObj['original_price'])
            printObject("hey004", bookJsonObj['discount_percentage'])
            printObject("hey005", bookJsonObj)
            books.append(bookJsonObj)
            # printObject("hey003",bookJsonObj['discount'])
            # print(jsonObj['original_price'])
            # print(jsonObj['discount_price'])
        print("The list printed sorting by discount_percentage: ")
        books = sorted(books, key=lambda i: i['discount_percentage'], reverse=True)
        print(books)

if __name__ == "__main__":
    # execute_category()
    execute_discount()
