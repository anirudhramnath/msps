#! /usr/bin/env python

import copy

class NotASubsequence(Exception):
    pass


def actual_support(transactions, sequence):
    count = 0
    for transaction in transactions:
        if is_subsequence(transaction, sequence):
            count += 1
    return count

def is_subsequence(transaction, sequence):
    transaction = copy.deepcopy(transaction)
    sequence = copy.deepcopy(sequence)
    while len(sequence) != 0 and len(transaction) != 0:
        if is_subset(transaction[0], sequence[0]):
            transaction.pop(0)
            sequence.pop(0)
        else:
            transaction.pop(0)
    return len(sequence) == 0

def is_subset(super_set, sub_set):
    for ele in sub_set:
        if ele not in super_set:
            return False
    return True

def get_projected_database(transactions, sequence, frequent_elements):
    S = []
    for transaction in transactions:

        try:
            S.append(get_projected_sequence(transaction, sequence, frequent_elements))
        except:
            pass

    return S


def get_projected_sequence(transaction, sequence, frequent_elements):
    remaining_itemset = []
    transaction = copy.deepcopy(transaction)
    sequence = copy.deepcopy(sequence)
    if is_subsequence(transaction, sequence):
        while len(sequence) != 0:
            if len(sequence) != 1:
                if is_subset(transaction[0], sequence[0]):
                    transaction.pop(0)
                    sequence.pop(0)
                else:
                    transaction.pop(0)
            else:
                if is_subset(transaction[0], sequence[0]):
                    (current_transaction, current_sequence) = (transaction[0], sequence[0])
                    if len(current_transaction) - 1 > current_transaction.index(current_sequence[-1]):
                        remaining_itemset = ['_'] + current_transaction[current_transaction.index(current_sequence[-1]) + 1:]
                    transaction.pop(0)
                    sequence.pop(0)
                else:
                    transaction.pop(0)
    else:
        raise NotASubsequence()


    if len(remaining_itemset) != 0:
        transaction = [remaining_itemset]+transaction

    if len(transaction) > 0:
        return transaction
    else:
        return [['_']]

def remove_infrequent_items(sequence, frequent_elements):
    return_sequence = []
    for itemset in sequence:
        itemset_copy = copy.deepcopy(itemset)
        for ele in itemset:
            if ele not in frequent_elements:
                itemset_copy.remove(ele)
        return_sequence.append(itemset_copy)
    return return_sequence

def remove_item_from_transaction(transaction, item):
    new_transaction = []
    for itemset in transaction:
        filtered_item_set = [i for i in itemset if i != item]
        if len(filtered_item_set) > 0:
            new_transaction.append(filtered_item_set)
    return new_transaction

def find_candidate_for_ele_with_x(transaction_database, sequence, frequent_items):
    for transaction in transaction_database:
        for itemset in transaction:
            if itemset[0] == '_':
                for x in itemset[1:]:
                    if x in frequent_items:
                        subsets.append(x)
            else:
                if item in itemset:
                    i = itemset.index(item)
                    _item_set = itemset[i+1:]
                    for x in _item_set:
                        if x in frequent_items:
                            subsets.append(x)

def find_candidate_for_ele_x(transaction, sequence, frequent_items):
    list_of_x = []
    transaction = copy.deepcopy(transaction)
    if transaction[0][0] == '_':
       transaction.pop(0)
    for itemset in transaction:
        for ele in itemset:
            if ele in frequent_items:
                list_of_x.append(ele)
    return list(set(list_of_x))


def find_candidate_for_ele_with_x1(transaction, sequence, frequent_items):
    list_of_x = []
    if transaction[0][0] == '_':
        for ele in transaction[0][1:]:
            if ele in frequent_items:
                list_of_x.append(ele)
    if is_subsequence(transaction, sequence):
        transaction = get_projected_sequence(transaction, sequence, frequent_items)
        list_of_x = list_of_x + find_candidate_for_ele_with_x1(transaction, sequence, frequent_items)
    return list(set(list_of_x))

def get_S_K_for_item(transactions, item, SDC, item_list):
    sup = calculate_support_for_elements(item_list, transactions)
    resulting_transactions = []
    for transaction in transactions:
        filtered_transaction = prepare_transaction(transaction, item, SDC, item_list, sup)
        if filtered_transaction != None:
            resulting_transactions.append(filtered_transaction)
    return resulting_transactions

def prepare_transaction(transaction, item, SDC, item_list, support_dict):
    if not is_subsequence(transaction, [[item]]):
        return None
    item_list = copy.deepcopy(item_list)
    item_list.remove(item)
    for itemj in item_list:
        if support_dict[itemj] - support_dict[item] > SDC:
            transaction = remove_item_from_transaction(transaction, itemj)
    return transaction

def remove_item_from_transactions(item, transactions):
    new_transactions = []
    for transaction in transactions:
        for itemset in transaction:
            try:
                while True:
                    itemset.remove(item)
            except ValueError:
                pass
            transaction = [i for i in transaction if len(i) > 0]
        if len(transaction) > 0:
            new_transactions.append(transaction)
    return new_transactions

def calculate_support_for_elements(items, transactions):
    sup = {}
    for item in items:
        sup[item] = float(actual_support(transactions, [[item]]))/len(transactions)
    return sup

class SequenceGenerator:
    def __init__(self, item, item_mis_as_int, transaction_subset, frequent_items, list_of_items, support_for_items, sdc):
        self.transaction_subset = transaction_subset
        self.frequent_sequences = {}
        self.list_of_items = list_of_items
        self.item = item
        self.item_mis_as_int = item_mis_as_int
        self.sequence_transaction_list = []
        self.frequent_items = frequent_items
        self.frequent_items_for_this_subset = self.get_frequent_items()
        self.frequent_items_list_for_this_subset = [i[0] for i in self.frequent_items_for_this_subset]
        self.support_for_items = support_for_items
        self.sdc = sdc
        for item, list_of_transactions in self.frequent_items_for_this_subset:
            self.get_candidate_for_sequence([[item]], self.support_for_items[item], self.support_for_items[item], list_of_transactions)

    def get_frequent_items(self):
        frequent_items_for_this_subset = []
        for item in self.list_of_items:
            list_of_transactions = []
            for transaction in self.transaction_subset:
                if is_subsequence(transaction, [[item]]):
                    list_of_transactions.append(copy.deepcopy(transaction))
            if len(list_of_transactions) >= self.item_mis_as_int:
                frequent_items_for_this_subset.append((item, list_of_transactions))
        return frequent_items_for_this_subset

    def get_candidate_for_sequence(self, sequence, sequence_min, sequence_max, transactions):
        transaction_mapping_for_first_condition = {}
        transaction_mapping_for_second_condition = {}
        element_min_max_for_first_condition = {}
        element_min_max_for_second_condition = {}
        sequence_transaction_list = []
        for transaction in transactions:
            try:

                projected_sequence = get_projected_sequence(transaction, sequence, self.frequent_items_list_for_this_subset)

                for candidate_element in list(set(find_candidate_for_ele_with_x1(projected_sequence, sequence, self.frequent_items_list_for_this_subset))):
                    extended_sequence = copy.deepcopy(sequence)
                    extended_sequence[-1].append(candidate_element)
                    projected_sequence = get_projected_sequence(transaction, extended_sequence, self.frequent_items_list_for_this_subset)
                    temp_sequence_min = sequence_min
                    temp_sequence_max = sequence_max


                    if is_subsequence(extended_sequence, [[self.item]]) or is_subsequence(projected_sequence, [[self.item]]):

                        if not(self.support_for_items[candidate_element] >= sequence_min and self.support_for_items[candidate_element] <= sequence_max):
                            if self.support_for_items[candidate_element] <= sequence_min:
                                temp_sequence_min = self.support_for_items[candidate_element]
                            if self.support_for_items[candidate_element] >= sequence_max:
                                temp_sequence_max = self.support_for_items[candidate_element]

                        if temp_sequence_max - temp_sequence_min <= self.sdc:
                            element_min_max_for_first_condition[candidate_element] = (temp_sequence_min, temp_sequence_max)

                        try:
                            _ = transaction_mapping_for_first_condition[candidate_element]
                            transaction_mapping_for_first_condition[candidate_element].append(transaction)
                        except KeyError:
                            transaction_mapping_for_first_condition[candidate_element] = [transaction]

                tmp_list = list(set(find_candidate_for_ele_x(projected_sequence, sequence, self.frequent_items_list_for_this_subset)))

                for candidate_element in tmp_list:
                    extended_sequence = copy.deepcopy(sequence)
                    extended_sequence.append([candidate_element])
                    projected_sequence = get_projected_sequence(transaction, extended_sequence, self.frequent_items_list_for_this_subset)
                    temp_sequence_min = sequence_min
                    temp_sequence_max = sequence_max


                    if is_subsequence(extended_sequence, [[self.item]]) or is_subsequence(projected_sequence, [[self.item]]):
                        if not(self.support_for_items[candidate_element] >= sequence_min and self.support_for_items[candidate_element] <= sequence_max):
                            if self.support_for_items[candidate_element] <= sequence_min:
                                temp_sequence_min = self.support_for_items[candidate_element]
                            if self.support_for_items[candidate_element] >= sequence_max:
                                temp_sequence_max = self.support_for_items[candidate_element]
                        temp_sdc = temp_sequence_max - temp_sequence_min
                        if temp_sequence_max - temp_sequence_min <= self.sdc:
                            element_min_max_for_second_condition[candidate_element] = (temp_sequence_min, temp_sequence_max)
                        try:
                            _ = transaction_mapping_for_second_condition[candidate_element]
                            transaction_mapping_for_second_condition[candidate_element].append(transaction)
                        except KeyError:
                            transaction_mapping_for_second_condition[candidate_element] = [transaction]

            except NotASubsequence:
                pass

        for element in element_min_max_for_first_condition:
            extended_sequence = copy.deepcopy(sequence)
            extended_sequence[-1].append(element)
            if len(transaction_mapping_for_first_condition[element]) >= self.item_mis_as_int:
                self.get_candidate_for_sequence(extended_sequence, element_min_max_for_first_condition[element][0], element_min_max_for_first_condition[element][1], transaction_mapping_for_first_condition[element])
                self.sequence_transaction_list.append((extended_sequence, transaction_mapping_for_first_condition[element]))
        for element in element_min_max_for_second_condition:
            extended_sequence = copy.deepcopy(sequence)
            extended_sequence.append([element])
            if len(transaction_mapping_for_second_condition[element]) >= self.item_mis_as_int:
                self.get_candidate_for_sequence(extended_sequence, element_min_max_for_second_condition[element][0], element_min_max_for_second_condition[element][1], transaction_mapping_for_second_condition[element])
                self.sequence_transaction_list.append((extended_sequence, transaction_mapping_for_second_condition[element]))
