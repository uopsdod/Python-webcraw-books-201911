#!/usr/bin/env python3

import json
import io
import collections

def execute_category():
    with io.open('output/crawlbook.jl', 'r', encoding='utf-8-sig') as f:
        # ...
        dict = {};  # put it up here to record all data
        count = 0;
        for line in f:
            line = line.encode('utf-8-sig')[3:].decode('utf-8-sig')  # this works too
            # line = line.encode('utf-8')[3:].decode('utf-8')  # this works too
            jsonObj = json.loads(line)

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

        # sort the books according to the dictionary key
        dict_filtered = collections.OrderedDict(sorted(dict.items()))

        # show result
        print(dict_filtered)
        # for k, v in od.items(): print(k, v)
        print("category count {:d} ".format(count))

def printObject(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)

if __name__ == "__main__":
    execute_category()
