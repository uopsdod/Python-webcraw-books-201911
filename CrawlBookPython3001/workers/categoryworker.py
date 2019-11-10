#!/usr/bin/env python3

import json
import io
import collections


class Categoryworker:
    """A class to process category-related information"""
    def execute_category(self, source_file_path):
        output_path = 'CrawlBookPython3001/output/categoryworker_result.txt'
        encoding_str = 'utf-8-sig'
        with io.open(source_file_path, 'r', encoding=encoding_str) as f, \
                io.open(output_path, 'w', encoding=encoding_str) as fw:
            dict = {}  # put it up here to record all data
            count = 0
            for line in f:
                # solve bom issue
                line = line.encode(encoding_str)[3:].decode(encoding_str)
                bookJsonObj = json.loads(line)

                # skip inaccessible information
                if 'LOGIN_REQUIRED' == bookJsonObj['category']:
                    continue

                # assemble category key list
                count += 1  # for debugging purpose
                category_keys = list()
                for category in bookJsonObj['category'].split(">"):
                    if len(category_keys) == 0:
                        category_keys.append(category)
                    else:
                        category_keys.append(category_keys[-1]+"/"+category)

                # increment category count
                for key in category_keys:
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


def print_object(identifier, obj):
    print(identifier)
    print(type(obj))
    print(obj)

if __name__ == "__main__":
    Categoryworker().execute_category()
