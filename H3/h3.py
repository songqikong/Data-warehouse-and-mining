class PrefixSpan:
    def __init__(self, min_support):
        self.min_support = min_support
        self.frequent_patterns = []

    def prefix_span(self, database, pattern=None, support=None):
        if pattern is None:
            pattern = []
        if support is None:
            support = {}

        # 获取频繁项目
        frequent_items = self.get_frequent_items(database, pattern, support)
        for item in frequent_items:
            new_pattern = pattern + [item]
            new_database = self.get_projected_database(database, new_pattern)
            new_support = self.get_support(new_database)

            # 检查支持度是否满足要求
            if new_support >= self.min_support:
                self.frequent_patterns.append((new_pattern, new_support))

                # 递归进行下一轮查找
                self.prefix_span(new_database, new_pattern, new_support)

    def get_frequent_items(self, database, pattern, support):
        items_count = {}
        for sequence in database:
            is_prefix = True
            for i, item in enumerate(pattern):
                if i >= len(sequence) or sequence[i] != item:
                    is_prefix = False
                    break
            if is_prefix and len(sequence) > len(pattern):
                next_item = sequence[len(pattern)]
                items_count[next_item] = items_count.get(next_item, 0) + 1
        return [item for item, count in items_count.items() if count >= self.min_support]

    def get_projected_database(self, database, pattern):
        projected_database = []
        for sequence in database:
            i = 0
            for item in sequence:
                if i < len(pattern) and item == pattern[i]:
                    i += 1
            if i == len(pattern):
                projected_database.append(sequence[i:])
        return projected_database

    def get_support(self, database):
        return len(database)

    def mine(self, database):
        self.frequent_patterns = []
        self.prefix_span(database)
        return self.frequent_patterns

class SPMFSequenceDatabaseParser:
    @staticmethod
    def parse_file(file_path, max_lines=None):
        sequences = []
        with open(file_path, 'r') as file:
            current_sequence = []
            for line_number, line in enumerate(file, start=1):
                if max_lines is not None and line_number > max_lines:
                    break

                items = list(map(int, line.strip().split()))
                # 如果行以 -1 结尾，表示一个项结束；如果以 -2 结尾，表示一个序列结束
                if items[-1] == -1:
                    current_sequence.extend(items[:-1])
                elif items[-1] == -2:
                    current_sequence.extend(items[:-1])
                    sequences.append(current_sequence)
                    current_sequence = []
                else:
                    current_sequence.extend(items)

        return sequences


# 示例用法
if __name__ == "__main__":
    file_path = "data.slen_10.tlen_1.seq.patlen_2.lit.patlen_8.nitems_5000_spmf.txt"
    max_lines_to_read = 1000  # 设定你想要读取的行数，或者设为 None 读取整个文件
    
    # 解析数据集
    sequence_database = SPMFSequenceDatabaseParser.parse_file(file_path, max_lines=max_lines_to_read)

    # 设置最小支持度阈值
    min_support = 2

    # 使用 PrefixSpan 进行挖掘
    prefix_span = PrefixSpan(min_support)
    frequent_patterns = prefix_span.mine(sequence_database)

    # 打印频繁模式及其支持度
    print(f"Frequent Patterns with support >= {min_support}:")
    for pattern, support in frequent_patterns:
        print(f"Pattern: {pattern}, Support: {support}")
