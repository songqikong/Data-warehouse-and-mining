import os
import numpy as np
import time
from itertools import combinations

# 设置支持度
support_rate = 0.001
# 设置频繁几项式
n = 2
# 设置读取几条transaction
max_line = 3000
file_name = os.path.join("tdb2.dat")
datalist = []
flatdata = np.array([], dtype=str)
line_count = 0

# with open(file_name, 'r') as f:
#     for line in f:
#         line = line.split()
#         _data = [int(x) for x in line]
#         datalist.append(_data)
#         flatdata = np.append(flatdata, _data)

#         line_count += 1

#         if line_count >= max_line:
#             break  # 当达到100行时停止读取

# paper_dict = {}

with open('outputacm.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line_count == max_line:
            break;
        if line != '\n' and line[1]=="@":
            # print(line)
            authors = line[2:-2]
            if authors == '':
                continue
            authors_list = authors.split(',')
            datalist.append(authors_list)
            flatdata = np.append(flatdata, authors_list)
            line_count += 1
            # paper_dict[line_count] = authors_list
        else:
            continue;

data = np.array(datalist, dtype=object)

begin_time = time.perf_counter()

# 查找data中所有唯一项，并分别统计这些唯一项在data中出现的次数
unique, counts = np.unique(flatdata, return_counts=True)

# 通过向量操作使得小于支持度的值去除
flag = np.where(counts < support_rate * max_line, 0, 1)
# 将flag中为0的项的index为索引，删除unique中对应索引的项。
one_frequent = unique[flag == 1]
one_frequent_counts = counts[flag == 1]
# one_frequent = unique * flag

print("####One_frequent")
for i in range(len(one_frequent)):
    print(f'Frequent itemset: ({one_frequent[i]}) Support: {one_frequent_counts[i]}')
# print("****One_frequent")
# 将counts中小于support_rate*max_line的项去除，将one_frequent中为0的项去除
# one_frequent_counts = np.delete(counts, np.where(counts < support_rate * max_line))
# one_frequent = np.delete(one_frequent, np.where(counts < support_rate * max_line))

step = 1

if n == 1:
    for i in range(len(one_frequent)):
        print(f'Frequent itemset: ({one_frequent[i]}) Support: {one_frequent_counts[i]}')

frequent_counts = one_frequent_counts
frequent = one_frequent

while step < n:
    step += 1
    if step == 2:
        combinations_list = list(combinations(frequent, 2))
        frequent = np.array(combinations_list)
        frequent_counts = np.zeros(len(combinations_list), dtype=int)
        for frequent_index, frequent_item in enumerate(frequent):
            for transaction_index, transaction in enumerate(data):
                if (frequent_item[0] in transaction) and (frequent_item[1] in transaction):
                    frequent_counts[frequent_index] += 1
        
        delete_indices = np.where(frequent_counts < support_rate * max_line)

        # 删除a中与b中值为零的项对应的行
        frequent = np.delete(frequent, delete_indices, axis=0)
        frequent_counts = np.delete(frequent_counts, delete_indices)
        print("#### Two _frequent")
        for i in range(len(frequent)):
            print(f'Frequent itemset: {frequent[i]} Support: {frequent_counts[i]}')
    elif step > 2:
        new_frequent = []
        for i, list_i in enumerate(frequent):
            for j, item_j in enumerate(one_frequent):
                if item_j in list_i:
                    continue
                new_list = list(list_i)
                new_list.append(item_j)
                new_list.sort()
                if tuple(new_list) not in new_frequent:
                    new_frequent.append(tuple(new_list))
        frequent = np.array(new_frequent)
        frequent_counts = np.zeros(len(new_frequent), dtype=int)
        for frequent_index, frequent_item in enumerate(frequent):
            for transaction_index, transaction in enumerate(data):
                if all(item in transaction for item in frequent_item):
                    frequent_counts[frequent_index] += 1

        delete_indices = np.where(frequent_counts < support_rate * max_line)

        # 删除a中与b中值为零的项对应的行
        frequent = np.delete(frequent, delete_indices, axis=0)
        frequent_counts = np.delete(frequent_counts, delete_indices)

        if len(frequent) == 0:
            print("没有 " + str(step) + " 频繁项集了")
            break
        print("#### {} _frequent".format(str(step)))
        for i in range(len(frequent)):
            print(f'Frequent itemset: {frequent[i]} Support: {frequent_counts[i]}')
        # print("**** {} _frequent".format(str(i)))
end_time = time.perf_counter()

print('程序运行时间:%s毫秒' % ((end_time - begin_time)*1000))


#implement a Chi-Squared Test to evaluate the frequent items
