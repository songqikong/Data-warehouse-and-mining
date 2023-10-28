import os
import numpy as np
from itertools import combinations

# 设置支持度
support_rate = 0.2

# 设置频繁几项式
i = 3

file_name = os.path.join("tdb2.dat")

datalist = []

# io input tdb2.dat
line_count = 0
# 设置读取几条transaction
max_line = 100

with open(file_name, 'r') as f:
    for line in f:
        line = line.split()
        _data = [int(x) for x in line]
        datalist.append(_data)

        line_count += 1

        if line_count >= max_line:
            break  # 当达到100行时停止读取

data = np.array([np.array(lst) for lst in datalist])

# 计算频繁项集
def eclat(data, min_support, k):
    items = {}
    for transaction in data:
        for item in transaction:
            if item in items:
                items[item].append(transaction)
            else:
                items[item] = [transaction]

    frequent_items = {}
    find_frequent_items(items, set(), frequent_items, min_support, k)

    return frequent_items

def find_frequent_items(items, prefix, frequent_items, min_support, k):
    if len(prefix) >= k:
        return

    for item, transactions in items.items():
        new_prefix = prefix.copy()
        new_prefix.add(item)
        support = calculate_support(transactions, data)
        if support >= min_support:
            frequent_items[tuple(new_prefix)] = support
            new_items = {}
            for i in range(item + 1, max(items.keys()) + 1):
                if i in items:
                    new_transactions = [t for t in items[i] if all(x in t for x in new_prefix)]
                    if len(new_transactions) >= min_support:
                        new_items[i] = new_transactions
            find_frequent_items(new_items, new_prefix, frequent_items, min_support, k)

def calculate_support(transactions, data):
    count = 0
    for transaction in data:
        if all(item in transaction for item in transactions):
            count += 1
    return count

frequent_items = eclat(data, support_rate, i)

for item_set, support in frequent_items.items():
    print(f"Item Set: {item_set}, Support: {support}")
