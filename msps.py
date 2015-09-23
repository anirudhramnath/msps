#!/usr/bin/env python

import parsefile
import utilities as util
from pprint import pprint
import math


""" Some constants """
INPUT_FILE_NAME = 'data.txt'
PARAM_FILE_NAME = 'para.txt'

def main():
    data = parsefile.parse_input_file(INPUT_FILE_NAME)
    mis, sdc = parsefile.parse_param_file(PARAM_FILE_NAME)
    
    """ Step 1: Find frequent items """
    frequent_items = find_frequent(data, mis, sdc)

    """ Step 2: Sort frequent items in ascending order according to their MIS value """
    frequent_items.sort(key=lambda x: x[1])

    # remove MIS values, and just retain item ID
    frequent_items = [x[0] for x in frequent_items]
    
    for item in frequent_items:
        #print(item)
        item_mis_as_int = math.ceil(mis[item]*len(data))
        transaction_subset = util.get_S_K_for_item(data, item, sdc, list(mis))
        #print(item, item_mis_as_int)
        #pprint(transaction_subset)
        sequence_generator = util.SequenceGenerator(item, item_mis_as_int, transaction_subset, frequent_items, list(mis))
        for i,j in sequence_generator.sequence_transaction_list:
            pass
            print(i)
        
        data = util.remove_item_from_transactions(item, data)
        #print(data)
        #print('\n\n')
        
    """ Step 3: Generate projected database 
    for item in frequent_items:
        S_k = util.get_projected_database(data, [[item]], frequent_items)

        if '44' == item:
            subsets = []

            for transaction in S_k:
                for itemset in transaction:
                    if itemset[0] == '_':
                        for x in itemset[1:]:
                            if x in frequent_items:
                                s = [[item, x]]
                                subsets.append(s)
                    else:
                        if item in itemset:
                            i = itemset.index(item)
                            _item_set = itemset[i+1:]
                            for x in _item_set:
                                if x in frequent_items:
                                    s = [[item, x]]
                                    subsets.append(s)

                        for x in itemset:
                            if x in frequent_items:
                                s = []
                                s.append([item])
                                s.append([x])
                                subsets.append(s)
            pprint (subsets)
    """

def r_prefix_span(item, sequence, data, mis_support):
    pass

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

if __name__ == '__main__':
    main()
