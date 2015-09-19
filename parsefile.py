#!/usr/bin/env python

import re


def parsefile(filename):
    result = []

    with open(filename, 'r') as f:
        for line in f:
            data = line.strip()[1:-1]
            m = re.findall('(?:\{([\d\s,]+)(?=\}))+', data)
            
            if len(m) > 0:
                row = []
                for item in m:
                    transaction = [int(x.strip()) for x in item.split(',')]
                    row.append(transaction)

                result.append(row)

        return result