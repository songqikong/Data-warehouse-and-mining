import os
import numpy as np
from itertools import combinations

# 设置支持度
support_rate = 0.05
# 设置频繁几项式
n = 2  # 这里假设你要挖掘频繁2项集，可以根据需要修改n的值
# 设置读取几条transaction
transaction_num = 100

file_name = os.path.join("tdb2.dat")

datalist = []

# io input tdb2.dat
line_count = 0

with open(file_name, 'r') as f:
    for line in f:
        line = line.split()
        _data = [int(x) for x in line]
        datalist.append(_data)

        line_count += 1

        if line_count >= transaction_num:
            break  # 当达到100行时停止读取

data = np.array([np.array(lst) for lst in datalist])

# 定义函数来生成候选项集
def generate_candidates(itemset, size):
    candidates = set()
    for item in itemset:
        for other in itemset:
            if item != other:
                candidate = tuple(sorted(set(item + other)))
                if len(candidate) == size:
                    candidates.add(candidate)
    return list(candidates)

# 定义函数来计算项集的支持度
def calculate_support(itemset, data):
    count = 0
    for transaction in data:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count / len(data)

# 初始化频繁项集及其支持度
frequent_itemsets = {}

# 生成频繁1项集
candidates = [(i,) for i in range(1, 1001)]
for candidate in candidates:
    support = calculate_support(candidate, data)
    if support >= support_rate:
        frequent_itemsets[candidate] = support

# 生成频繁n项集
for size in range(2, n + 1):
    candidates = generate_candidates(list(frequent_itemsets.keys()), size)
    for candidate in candidates:
        support = calculate_support(candidate, data)
        if support >= support_rate:
            frequent_itemsets[candidate] = support

# 输出指定的频繁n项集
for itemset, support in frequent_itemsets.items():
    if len(itemset) == n:
        print("Frequent itemset:", itemset, "Support:", int(support*transaction_num))
