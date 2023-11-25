import pandas as pd

# 定义一个类来表示序列模式树的节点
class TreeNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}


def load_data(filename):
    # 读取SPMF格式的数据集
    with open(filename, 'r') as file:
        lines = file.readlines()

    sequences = []
    for line in lines:
        items = line.strip().split(' -1 ')
        sequence = [list(map(int, item.split())) for item in items if item]
        sequences.append(sequence)

    return sequences


def get_frequent_items(sequence, min_support):
    # 计算序列中每个项的支持计数
    item_counts = {}
    for transaction in sequence:
        for item in transaction:
            # Convert the list to a tuple to make it hashable
            item_tuple = tuple(item)

            if item_tuple in item_counts:
                item_counts[item_tuple] += 1
            else:
                item_counts[item_tuple] = 1

    # 筛选出支持计数大于等于最小支持度的项
    frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}

    return frequent_items



def build_prefix_span_tree(sequence, min_support, root):
    frequent_items = get_frequent_items(sequence, min_support)

    for item, count in frequent_items.items():
        new_sequence = []
        for transaction in sequence:
            if item in transaction:
                # 获取以当前项为前缀的子序列
                index = transaction.index(item)
                new_sequence.append(transaction[index + 1:])

        # 在前缀树上添加新节点
        child_node = TreeNode(item, count, root)
        root.children[item] = child_node

        # 递归构建子树
        build_prefix_span_tree(new_sequence, min_support, child_node)


def prefix_span(sequence, min_support):
    root = TreeNode(None, 0, None)
    build_prefix_span_tree(sequence, min_support, root)
    return root


def print_tree(node, level=0):
    # 递归打印前缀树
    if node.item is not None:
        print('  ' * level, f'{node.item}:{node.count}')
    for child_item, child_node in node.children.items():
        print_tree(child_node, level + 1)


if __name__ == '__main__':
    # 替换为你的SPMF格式数据集文件路径
    dataset_file = 'data.slen_10.tlen_1.seq.patlen_2.lit.patlen_8.nitems_5000_spmf.txt'
    min_support = 50
    sequences = load_data(dataset_file)
    root_node = prefix_span(sequences, min_support)

    print_tree(root_node)
