# Homework 1

### Q1. A database has 5 transactions. Let min_sup = 60% and min_conf = 80%.

| *TID*  | *items bought*        |
| ------ | --------------------- |
| *T100* | *{M, O, N, K, E, Y}*  |
| *T200* | *{D, O, N, K, E, Y }* |
| *T300* | *{M, A, K, E}*        |
| *T400* | *{M, U, C, K, Y}*     |
| *T500* | *{C, O, K, I ,E}*     |

#### (a) Find all frequent itemsets using Apriori algorithm.

//support threshold = 5 * 0.6 = 3

//confidence threshold = 5 * 0.8 = 4

<u>(1)find 1 frequent candidate & support Item</u>

|  A   |  C   |  D   |  E   |  I   |  K   |  M   |  N   |  O   |  U   |  Y   |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  1   |  2   |  1   |  4   |  1   |  5   |  5   |  2   |  4   |  1   |  4   |

|  E   |  K   |  M   |  O   |  Y   |
| :--: | :--: | :--: | :--: | :--: |
|  4   |  5   |  5   |  4   |  4   |

<u>(2)find 2 frequent  candidate & support Item</u>

|  EK  |  EM  |  EO  |  EY  |  KM  |  KO  |  KY  |  MO  |  MY  |  OY  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  4   |  2   |  3   |  2   |  3   |  3   |  3   |  1   |  2   |  2   |

|  EK  |  EO  |  KM  |  KO  |  KY  |
| :--: | :--: | :--: | :--: | :--: |
|  4   |  3   |  3   |  3   |  3   |

<u>(3)find 3 frequent  candidate & support Item</u>

| EKO  | EKM  | EKY  | EOM  | EOY  | KMO  | KMY  | KOY  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  3   |  2   |  2   |  1   |  2   |  1   |  2   |  2   |

| EKO  |
| :--: |
|  3   |

So we get the total frequent itemset:

<u>**T = {E  K  M  O  Y EK  EO  KM  KO  KY EKO}**</u>



#### (b) List all of the strong association rules

**For 3-frequent itemset:**

Con(EK|O) = S(EKO)/S(EK) = 0.75 ❌

Con(EO|K) = S(EKO)/S(EO) = 1 ✔

Con(OK|E) = S(EKO)/S(OK) = 1 ✔

**For 2-frequent itemset:**

Con(E|K) = S(EK)/S(E) = 1 ✔

Con(K|E) = S(EK)/S(K) = 0.8 ✔

**......Only two of them**

## Q2. (Implementation project) Implement two frequent itemset mining algorithms selected from: (1)  Apriori, (2) FP-growth, and (3) Eclat (mining using vertical data format), using a programming  language that you are familiar with. Compare the performance of each algorithm with two given  datasets.

#### (a) Apriori

代码思路：

设置超参数，文件IO读入数据库文件，设置读取多少行transaction：

```python
# 设置支持度
support_rate = 0.06
# 设置频繁几项式
n = 3
# 设置读取几条transaction
max_line = 100

with open(file_name, 'r') as f:
    for line in f:
        line = line.split()
        _data = [int(x) for x in line]
        datalist.append(_data)
        flatdata = np.append(flatdata, _data)

        line_count += 1

        if line_count >= max_line:
            break  # 当达到100行时停止读取
```

首先计算1频繁项集

```python
# data = np.array([np.array(lst) for lst in datalist])
data = np.array(datalist, dtype=object)

begin_time = time.perf_counter()
# 查找data中所有唯一项，并分别统计这些唯一项在data中出现的次数
unique, counts = np.unique(flatdata, return_counts=True)

# 通过向量操作使得小于支持度的值去除
flag = np.where(counts < support_rate * max_line, 0, 1)
one_frequent = unique * flag

# 将counts中小于support_rate*max_line的项去除，将one_frequent中为0的项去除
one_frequent_counts = np.delete(counts, np.where(counts < support_rate * max_line))
one_frequent = np.delete(one_frequent, np.where(counts < support_rate * max_line))

```

然后计算2频繁项集及n频繁项集，之所以分开2频繁项集及n频繁项集是因为1频繁项集的每一项并不是list，而是int。

```python
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
        print(frequent)
        print(frequent_counts)
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
        print(frequent)
        print(frequent_counts)
```

**实验：**

读取1000条，计算 2 频繁项，支持率为 0.01：

![image-20231028002353517](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20231028002353517.png)

读取100条，计算 2 频繁项，支持率为 0.05：

![image-20231028003409292](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20231028003409292.png)

读取100条，计算 3 频繁项，支持率为 0.08：

![image-20231028004132987](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20231028004132987.png)

读取100条，计算 3 频繁项，支持率为 0.06，这下终于有3 频繁项了：

![image-20231028004256471](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20231028004256471.png)

其他超参数的实验不做了，太慢了。

#### (b) Eclat 
