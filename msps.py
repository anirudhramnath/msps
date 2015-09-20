#!/usr/bin/env python

import parsefile
import utilities as util
from pprint import pprint

""" Some constants """
INPUT_FILE_NAME = 'data.txt'
PARAM_FILE_NAME = 'para.txt'

def main():
    data = parsefile.parse_input_file(INPUT_FILE_NAME)
    mis, sdc = parsefile.parse_param_file(PARAM_FILE_NAME)

    """ Step 1: Find frequent items """
    frequent_items = step_one(data, mis, sdc)
    


""" Finds frequent items
    returns: list of frequent items """
def step_one(data, mis, sdc):
    frequent_items = list(mis.keys())

    # check each item to see if it's support is greater than MIS(item)
    total_transactions = float( len(data) )
    new_freq_items = []

    for item in frequent_items:
        support = float(util.actual_support(data, [[item]])) / total_transactions

        if support < mis[item]:
            frequent_items.remove(item)

    return frequent_items

if __name__ == '__main__':
    main()