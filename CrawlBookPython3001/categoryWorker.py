#!/usr/bin/env python3

import json
import io

with io.open('result.jl', 'r') as f:
    # ...
    for line in f:
        # line = line.encode('utf-8-sig')[3:].decode('utf-8-sig') # this works too
        line = line.encode('utf-8')[3:].decode('utf-8')  # this works too
        jsonObj = json.loads(line)
        print(jsonObj['book_name'])
        print(jsonObj)
