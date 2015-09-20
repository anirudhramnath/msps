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
        raise NotASubsequence()

def remove_infrequent_items(sequence, frequent_elements):
    return_sequence = []
    for itemset in sequence:
        itemset_copy = copy.deepcopy(itemset)
        for ele in itemset:
            if ele not in frequent_elements:
                itemset_copy.remove(ele)
        return_sequence.append(itemset_copy)
    return return_sequence

