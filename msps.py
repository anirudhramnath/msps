#!/usr/bin/env python

import parsefile
import utilities as util
from pprint import pprint
import math


""" Some constants """
INPUT_FILE_NAME = 'data.txt'
PARAM_FILE_NAME = 'para.txt'

final_output = {}

def main():
    data = parsefile.parse_input_file(INPUT_FILE_NAME)
    mis, sdc = parsefile.parse_param_file(PARAM_FILE_NAME)

    """ Step 1: Find frequent items """
    frequent_items = find_frequent(data, mis, sdc)

    """ Step 2: Sort frequent items in ascending order according to their MIS value """
    frequent_items.sort(key=lambda x: x[1])

    # remove MIS values, and just retain item ID
    frequent_items = [x[0] for x in frequent_items]

    # add level 1 items
    final_output[1] = []
    for item in frequent_items:
        final_output[1].append(([[item]], util.actual_support(data, [[item]])))

    for item in frequent_items:
        #print(item)
        item_mis_as_int = math.ceil(mis[item]*len(data))
        transaction_subset = util.get_S_K_for_item(data, item, sdc, list(mis))

        sequence_generator = util.SequenceGenerator(item, item_mis_as_int, transaction_subset, frequent_items, list(mis))
        for i,j in sequence_generator.sequence_transaction_list:
            temp = [item for sublist in i for item in sublist]

            if len(temp) not in final_output:
                final_output[len(temp)] = [(i, len(j))]
            else:
                final_output[len(temp)].append((i, len(j)))

            #print(i), len(j)

        data = util.remove_item_from_transactions(item, data)


    for k in sorted(final_output.keys()):
        print '\nThe number of length '+str(k)+' sequential patterns is '+ str(len(final_output[k]))
        for patterns in final_output[k]:
            print 'Pattern: '+pprint_result(str(patterns[0]))+' Count: '+str(patterns[1])

""" Finds frequent items
    returns: list of frequent items (item, mis_val) """
def find_frequent(data, mis, sdc):
    frequent_items = list(mis.keys())
    return_list = []

    # check each item to see if it's support is greater than MIS(item)
    total_transactions = float( len(data) )
    new_freq_items = []

    for item in frequent_items:
        support = float(util.actual_support(data, [[item]])) / total_transactions
        print 'Support of item ' + str(item) + ' is :' + str(support)
        if support >= mis[item]:
            return_list.append( (item, mis[item]) )


    return return_list

def pprint_result(pattern_str):
    pattern_str = pattern_str[1:-1]

    pattern_str = '{'.join(pattern_str.split('['))
    pattern_str = '}'.join(pattern_str.split(']'))

    result = '<' + pattern_str.replace("'", "") + '>'
    return result

if __name__ == '__main__':
    main()
