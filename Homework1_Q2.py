import os
import numpy as np
from itertools import combinations
# 设置支持度
support_rate = 0.1
# 设置频繁几项式
i=2

file_name = os.path.join("tdb2.dat")

data = np.array([], dtype=int) 

# io input tdb2.dat
line_count = 0
# 设置读取几条transaction
max_line = 100

with open(file_name, 'r') as f:
    for line in f:
        line = line.split()
        _data = [int(x) for x in line]
        # np.array(_data)
        # 将每个line存入data中
        data = np.append(data, _data)
        line_count += 1
        
        if line_count >= max_line:
            break  # 当达到100行时停止读取

      
# 查找data中所有唯一项，并分别统计这些唯一项在data中出现的次数

unique, counts = np.unique(data, return_counts=True)


# 通过向量操作使得小于支持度的值去除
flag = np.where(counts < support_rate * max_line, 0, 1)
one_frequent = unique * flag

# 将counts中小于support_rate*max_line的项去除，将one_frequent中为0的项去除
one_frequent_counts = np.delete(counts, np.where(counts < support_rate * max_line))
one_frequent = np.delete(one_frequent, np.where(counts < support_rate * max_line))

step = 1
if (i == 1):
    print(one_frequent_counts)
    print(one_frequent)
    
frequent_counts = one_frequent_counts
frequent= one_frequent
# print(len(one_frequent_counts))
while(step < i):
    step+=1;
    combinations_list = list(combinations(frequent, 2))
    # 计算STEP频繁项集
    frequent = np.array(combinations_list)
    frequent_counts = np.array(len(combinations_list), dtype=int)

    # print(len(frequent))
    for frequent_index, frequent_item in enumerate(frequent):
       for transaction_index, transaction in enumerate(data):
           if 


