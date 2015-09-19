def actual_support(transactions, sequence):
    count = 0
    for transaction in transactions:
        if is_subsequence(transaction, sequence):
            count += 1
    return count

def is_subsequence(transaction, sequence):
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
