#!/usr/bin/env python

import parsefile
import utilities as util
import math
import sys


""" Some constants """
INPUT_FILE_NAME = ''
PARAM_FILE_NAME = ''
OUTPUT_FILE_NAME = ''

final_output = {}

def main():
    data = parsefile.parse_input_file(INPUT_FILE_NAME)
    mis, sdc = parsefile.parse_param_file(PARAM_FILE_NAME)
    support_dict_for_elements = util.calculate_support_for_elements(list(mis), data)

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
        item_mis_as_int = math.ceil(mis[item]*len(data))
        transaction_subset = util.get_S_K_for_item(data, item, sdc, list(mis))

        sequence_generator = util.SequenceGenerator(item, item_mis_as_int, transaction_subset, frequent_items, list(mis),  support_dict_for_elements, sdc)
        for i,j in sequence_generator.sequence_transaction_list:
            temp = [item for sublist in i for item in sublist]

            if len(temp) not in final_output:
                final_output[len(temp)] = [(i, len(j))]
            else:
                final_output[len(temp)].append((i, len(j)))

        data = util.remove_item_from_transactions(item, data)


    with open(OUTPUT_FILE_NAME, 'w') as output_file:
        for k in sorted(final_output.keys()):
            output_file.write('\nThe number of length '+str(k)+' sequential patterns is '+ str(len(final_output[k])) + '\n\n')
            for patterns in final_output[k]:
                output_file.write('Pattern: '+pprint_result(str(patterns[0]))+' Count: '+str(patterns[1])+'\n')

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
    if len(sys.argv) != 4:
        print "Usage: python msps.py <data_file> <para_file> <output_file>"
        sys.exit()

    INPUT_FILE_NAME = sys.argv[1]
    PARAM_FILE_NAME = sys.argv[2]
    OUTPUT_FILE_NAME = sys.argv[3]

    main()
