#!/usr/bin/env python3

import json
import io
import collections

class Categoryworker:
    """A class to process category-related information"""
    def execute_category(self, source_file_path):
        with io.open(source_file_path, 'r', encoding='utf-8-sig') as f, io.open('CrawlBookPython3001/output/categoryworker_result.txt', 'w', encoding='utf-8-sig') as fw:
            dict = {};  # put it up here to record all data
            count = 0;
            for line in f:
                line = line.encode('utf-8-sig')[3:].decode('utf-8-sig')  # solve bom issue
                bookJsonObj = json.loads(line)

                # skip inaccessible information
                if 'LOGIN_REQUIRED' == bookJsonObj['category']:
                    continue;

                # assemble category key list
                count += 1 # for debugging purpose
                category_keylist = list()
                for category in bookJsonObj['category'].split(">"):
                    if len(category_keylist) == 0:
                        category_keylist.append(category)
                    else:
                        category_keylist.append(category_keylist[-1] + "/" + category)

                # increment category count
                for key in category_keylist:
                    if key in dict:
                        dict[key] += 1
                    else:
                        dict[key] = 1

            # sort the books according to the dictionary key
            dict_filtered = collections.OrderedDict(sorted(dict.items()))

            # show result
            print(dict_filtered)
            for k, v in dict_filtered.items():
                tmp_line = k + " " + str(v) + "\r\n"
                fw.write(tmp_line)
            print("category count {:d} ".format(count))

def printObject(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)

if __name__ == "__main__":
    Categoryworker().execute_category()
