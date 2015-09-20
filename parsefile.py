#!/usr/bin/env python

import re

""" This function return a list of transactions present in the input file """
def parse_input_file(filename):
    result = []

    with open(filename, 'r') as f:
        for line in f:
            data = line.strip()[1:-1]
            m = re.findall('(?:\{([\d\s,]+)(?=\}))+', data)

            if len(m) > 0:
                row = []

                for item in m:
                    transaction = [str(x.strip()) for x in item.split(',')]
                    row.append(transaction)

                result.append(row)

        return result


""" Function to parse parameter file
    Returns a tuple (dictionary of minsups, sdc) """
def parse_param_file(filename):
    result = {}
    sdc = 0.0

    with open(filename, 'r') as f:
        for line in f:

            if line.startswith('SDC'):
                sdc = float(line.split('=')[1].strip());

            data = line.strip()
            m = re.findall('(?:MIS\((\d+)\)\s+=\s+(.+))', data)

            if len(m) > 0:
                result[m[0][0]] = float(m[0][1])

        return result, sdc
